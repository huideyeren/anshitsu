from PIL import Image


def output_rgb(image: Image) -> Image:
    """
    output_rgb

    Outputs a monochrome image in RGB.

    Returns:
        Image: processed image.
    """
    if image.mode == "L":
        image = image.convert("RGB")
    return image
