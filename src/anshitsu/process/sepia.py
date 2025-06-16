from PIL import Image


def sepia(image: Image) -> Image:
    """
    sepia

    Outputs a monochrome image colored at sepia.

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
