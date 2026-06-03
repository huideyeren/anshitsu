import numpy as np
from PIL import Image


def orthochromatic(image: Image) -> Image:
    """
    Convert an image to orthochromatic-style grayscale.

    Orthochromatic film is less sensitive to red light and more sensitive to
    blue light than modern panchromatic film. This conversion darkens red tones
    and lifts blue tones to approximate that older monochrome response.

    Parameters:
        image: Image

    Returns:
        Image: processed image in L mode.
    """
    if image.mode == "L":
        return image

    rgb = np.array(image.convert("RGB"), dtype="float32")

    gamma = 2.2
    rgb_l = pow(rgb / 255.0, gamma)

    red = rgb_l[:, :, 0]
    green = rgb_l[:, :, 1]
    blue = rgb_l[:, :, 2]

    gray_l = 0.05 * red + 0.55 * green + 0.40 * blue
    gray = pow(gray_l, 1.0 / gamma) * 255

    return Image.fromarray(gray.astype("uint8"))
