import cv2
import torch
import numpy as np

from torchvision import transforms
from fba import pred

# import functools


# TODO
# change it later to improve quality of results
def generate_trimap(seg_mask, probs, size, conf_threshold):
    trimap = (probs > 0.05).astype(float) * 0.5

    pixels = 2 * size + 1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (pixels, pixels))

    erosion = cv2.erode(seg_mask, kernel, iterations=17)
    dilation = cv2.dilate(seg_mask, kernel, iterations=12)

    trimap = np.zeros_like(seg_mask)
    trimap[np.logical_and(probs > 0.1, probs < conf_threshold)] = 0.5
    trimap[dilation == 1] = 0.5
    trimap[probs > 0.99] = 1
    trimap[erosion == 1] = 1

    return trimap


def image_to_trimap(image, model):
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    preprocess = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
        ]
    )

    batch: torch.Tensor = preprocess(image).unsqueeze(0)

    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    batch = batch.to(device)
    model = model.to(device)

    with torch.no_grad():
        output: torch.Tensor = model(batch)["out"][0].softmax(dim=0)

    seg_mask = (output.argmax(0) != 0).cpu().numpy().astype(float)
    fg_probs = (1 - output[0]).cpu().numpy()

    return fba_trimap(generate_trimap(seg_mask, fg_probs, 2, 0.9))


def fba_trimap(trimap):
    h, w = trimap.shape
    fba_trimap = np.zeros((h, w, 2))
    fba_trimap[trimap == 1, 1] = 1
    fba_trimap[trimap == 0, 0] = 1
    return fba_trimap


def generate_fg_bg_alpha(fba_model, image, trimap) -> np.ndarray:
    return pred(np.array(image) / 255, trimap, fba_model)
