import io
from typing import Tuple

from PIL import Image


def resize_image(
    image_data: bytes, max_size: Tuple[int, int] = (800, 600)
) -> Tuple[bytes, int, int]:
    """
    Resizes the image to the specified maximum size while maintaining aspect ratio"""
    with Image.open(io.BytesIO(image_data)) as img:
        img.thumbnail(max_size)
        output = io.BytesIO()
        img.save(output, format=img.format)
        resized_data = output.getvalue()
        return resized_data, img.width, img.height
