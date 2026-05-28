from PIL import Image


def sepia(image: Image) -> Image:
    """
    Colorize a monochrome image with sepia tones.

    Returns:
        Image: processed image.
    """
    if image.mode == "L":
        image = Image.merge(
            "RGB",
            (
                image.point(lambda x: x * 247 / 255),
                image.point(lambda x: x * 225 / 255),
                image.point(lambda x: x * 194 / 255),
            ),
        )
    return image
