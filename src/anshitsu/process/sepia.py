from PIL import Image

def sepia(image: Image) -> Image:
    """
    sepia

    Outputs a monochrome image colored at sepia.

    Returns:
        Image: processed image.
    """
    if image.mode == "L":
        image = Image.merge("RGB",
            (
                image.point(lambda x: x * 240 / 255),
                image.point(lambda x: x * 200 / 255),
                image.point(lambda x: x * 145 / 255)
            )
        )
    return image