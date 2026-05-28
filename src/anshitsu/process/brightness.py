from PIL import Image, ImageEnhance


def brightness(image: Image, brightness: float) -> Image:
    """
    Adjust image brightness.

    Parameters:
        image: Image
        brightness: enhancement factor

    Returns:
        Image: processed image.
    """
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)
    return image
