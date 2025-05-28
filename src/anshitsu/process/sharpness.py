from PIL import Image, ImageEnhance


def sharpness(image: Image, sharpness: float) -> Image:
    """
    sharpness

    Fix sharpness.

    Parameters:
        image: Image
        sharpness: float

    Returns:
        Image: processed image.
    """
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpness)
    return image
