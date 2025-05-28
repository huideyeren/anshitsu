from typing import Tuple

from PIL import Image


def remove_alpha(image: Image) -> Image:
    """
    __rgba_convert

    Converts image data that contains transparency to image data that does not contain transparency.

    Returns:
        Image: processed image.
    """

    rgb_red_value: int = 255
    rgb_green_value: int = 255
    rgb_blue_value: int = 255
    rgb_white_color: Tuple[int, int, int] = (
        rgb_red_value,
        rgb_green_value,
        rgb_blue_value,
    )

    if image.mode == "RGBA":
        image.load()
        background = Image.new("RGB", image.size, rgb_white_color)
        background.paste(image, mask=image.split()[3])
        image = background
    if image.mode == "LA":
        image.load()
        background = Image.new("L", image.size, 255)
        background.paste(image, mask=image.split()[1])
        image = background
    return image
