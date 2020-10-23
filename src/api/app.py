from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import StreamingResponse

from pydantic import BaseModel

from PIL import Image
import numpy as np
import io

from ..utils import generate_fg_bg_alpha, image_to_trimap

from ..utils.models import fba_model, seg_model

router = APIRouter()


@router.post(
    "/removebg",
    response_class=StreamingResponse,
    response_description="Image background removed",
    responses={
        200: {
            "content": {"image/*": {"example": "(binary image data)"}},
        }
    },
)
async def get_alpha_mask(image_file: UploadFile = File(...)):

    if not "image" in image_file.content_type:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File is not an image"
        )

    image = Image.open(image_file.file)
    trimap = image_to_trimap(image, seg_model)

    fg, _, alpha = generate_fg_bg_alpha(fba_model, image, trimap)

    result = (np.dstack((fg, alpha)) * 255).astype(np.uint8)
    result = Image.fromarray(result, mode="RGBA")

    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(
        content=buffer,
        media_type="image/png",
    )
