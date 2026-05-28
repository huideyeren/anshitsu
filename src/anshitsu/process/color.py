from PIL import Image, ImageEnhance


def color(image: Image, color: float) -> Image:
    """
    Adjust image color.

    Parameters:
        image: Image
        color: enhancement factor

    Returns:
        Image: processed image.
    """
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(color)
    return image
