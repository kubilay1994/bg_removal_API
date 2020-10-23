from fba import build_model
from torchvision.models.segmentation import deeplabv3_resnet101


seg_model = deeplabv3_resnet101(pretrained=True).eval()


class Args:
    encoder = "resnet50_GN_WS"
    decoder = "fba_decoder"
    weights = "models/FBA.pth"


fba_model = build_model(Args()).eval()