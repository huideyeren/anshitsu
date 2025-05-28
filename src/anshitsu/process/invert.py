from PIL import Image, ImageOps


def invert(image: Image) -> Image:
    """
    invert

    Invert color.

    Parameters:
        image: Image

    Returns:
        Image: processed image.
    """
    return ImageOps.invert(image)
