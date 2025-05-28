from PIL import Image, ImageEnhance


def color(image: Image, color: float) -> Image:
    """
    contrast

    Fix color balance.

    Parameters:
        image: Image
        color: float

    Returns:
        Image: processed image.
    """
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(color)
    return image
