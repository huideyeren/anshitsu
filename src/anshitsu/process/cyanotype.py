from PIL import Image, ImageOps


def cyanotype(image: Image) -> Image:
    """
    cyanotype

    Outputs a monochrome image colored at prussian blue like cyanotype.

    Returns:
        Image: processed image.
    """
    if image.mode == "L":
        image = ImageOps.colorize(image, black=(26, 68, 114), white=(255, 255, 255))
    return image
