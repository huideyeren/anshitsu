import colorcorrect.algorithm as cca
from PIL import Image
from colorcorrect.util import to_pil, from_pil


def color_stretch(image: Image) -> Image:
    """
    Apply gray-world white balance and color stretching.

    Parameters:
        image: Image

    Returns:
        Image: processed image.
    """
    if image.mode == "L":
        return image
    return to_pil(cca.stretch(cca.grey_world(from_pil(image))))
