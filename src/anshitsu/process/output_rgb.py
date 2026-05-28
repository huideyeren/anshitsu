from PIL import Image


def output_rgb(image: Image) -> Image:
    """
    Convert a monochrome image to RGB.

    Returns:
        Image: processed image.
    """
    if image.mode == "L":
        image = image.convert("RGB")
    return image
