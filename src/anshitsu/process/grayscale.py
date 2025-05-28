from collections import namedtuple

import numpy as np
from PIL import Image


def grayscale(image: Image) -> Image:
    """
    grayscale

    Converts to grayscale based on the luminance in the CIE XYZ color space.

    Parameters:
        image: Image

    Returns:
        Image: processed image.
    """
    if image.mode == "L":
        return image

    rgb = np.array(image, dtype="float32")

    gamma = 2.2
    ColorMatrix = namedtuple("ColorMatrix", ("red", "green", "blue"))

    # Coefficients for luminance in CIE XYZ color space
    cie_xyz = ColorMatrix(0.2126, 0.7152, 0.0722)

    # Inverse Gamma Correction
    rgb_l = pow(rgb / 255.0, gamma)

    # Extract RGB values
    r, g, b = rgb_l[:, :, 0], rgb_l[:, :, 1], rgb_l[:, :, 2]

    # Convert to grayscale
    gray_l = cie_xyz.red * r + cie_xyz.green * g + cie_xyz.blue * b

    # gamma correction
    gray = pow(gray_l, 1.0 / gamma) * 255

    image = Image.fromarray(gray.astype("uint8"))

    return image
