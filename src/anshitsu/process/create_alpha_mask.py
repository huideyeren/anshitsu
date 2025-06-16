from typing import Union

from PIL import Image


def create_alpha_mask(image: Image) -> Union[Image, None]:
    """
    create_alpha_mask

    If image has alpha layer, create alpha mask.

    Parameters:
        image: Image

    Returns:
        Image: cutout alpha mask.
        None: Image has not alpha mask.
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
