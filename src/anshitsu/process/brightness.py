from PIL import Image, ImageEnhance


def brightness(image: Image, brightness: float) -> Image:
    """
    brightness

    Fix brightness.

    Parameters:
        image: Image
        brightness: float

    Returns:
        Image: processed image.
    """
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)
    return image
