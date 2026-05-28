from PIL import Image, ImageEnhance


def sharpness(image: Image, sharpness: float) -> Image:
    """
    Adjust image sharpness.

    Parameters:
        image: Image
        sharpness: enhancement factor

    Returns:
        Image: processed image.
    """
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpness)
    return image
