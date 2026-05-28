import colorcorrect.algorithm as cca
from PIL import Image
from colorcorrect.util import to_pil, from_pil


def color_auto_adjust(image: Image) -> Image:
    """
    Correct colors using the Automatic Color Equalization algorithm.

    This process is based on the 2002 paper on Automatic Color Equalization
    by Carlo Gatta and coauthors.

    Returns:
        Image: processed image.
    """
    if image.mode == "L":
        return image
    return to_pil(cca.automatic_color_equalization(from_pil(image)))
