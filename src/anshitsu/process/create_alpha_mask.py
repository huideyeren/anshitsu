from typing import Union

from PIL import Image


def create_alpha_mask(image: Image) -> Union[Image, None]:
    """
    Create an alpha mask from an image with an alpha channel.

    Parameters:
        image: Image

    Returns:
        Image: alpha mask.
        None: image has no alpha channel.
    """
    if image.mode == "RGBA":
        _, _, _, alpha = image.split()
        alpha_channel = 255
        alpha.paste(Image.new("L", image.size, alpha_channel), mask=alpha)
        return alpha
    elif image.mode == "LA":
        _, alpha = image.split()
        alpha_channel = 255
        alpha.paste(Image.new("L", image.size, alpha_channel), mask=alpha)
        return alpha
    else:
        return None
