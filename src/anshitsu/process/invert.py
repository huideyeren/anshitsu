from PIL import Image, ImageOps


def invert(image: Image) -> Image:
    """
    Invert image colors.

    Parameters:
        image: Image

    Returns:
        Image: processed image.
    """
    return ImageOps.invert(image)
