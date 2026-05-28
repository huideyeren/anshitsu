import numpy as np
from PIL import Image


def ashigara(image: Image) -> Image:
    """
    Apply a vivid, high-contrast color grade inspired by Fujifilm Velvia 100.

    Returns:
        Image: processed image.
    """
    rgb_image = image.convert("RGB")
    image_array = np.array(rgb_image, dtype="float32") / 255.0

    # Increase contrast with a mild S-curve.
    image_array = 3 * image_array**2 - 2 * image_array**3
    image_array = (image_array - 0.5) * 1.12 + 0.5

    red = image_array[:, :, 0] * 1.05 + 0.005
    green = image_array[:, :, 1] * 1.04 + 0.006
    blue = image_array[:, :, 2] * 1.08 + 0.008
    image_array = np.stack((red, green, blue), axis=2)

    luminance = (
        image_array[:, :, 0] * 0.299
        + image_array[:, :, 1] * 0.587
        + image_array[:, :, 2] * 0.114
    )
    saturation = 1.28
    image_array = luminance[:, :, np.newaxis] + (
        image_array - luminance[:, :, np.newaxis]
    ) * saturation

    image_array = np.clip(image_array, 0.0, 1.0)
    return Image.fromarray((image_array * 255).astype("uint8"))
