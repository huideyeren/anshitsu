import colorcorrect.algorithm as cca
from PIL import Image
from colorcorrect.util import to_pil, from_pil


def color_auto_adjust(image: Image) -> Image:
    """
    color_auto_adjust

    Use Color Auto Adjust algorithm.

    Returns:
        Image: processed image.
    """
    if image.mode == "L":
        return image
    return to_pil(cca.automatic_color_equalization(from_pil(image)))
