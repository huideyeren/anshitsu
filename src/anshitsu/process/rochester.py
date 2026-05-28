import numpy as np
from PIL import Image


def rochester(image: Image) -> Image:
    """
    Apply a warm, low-saturation color grade inspired by Kodak PORTRA 400.

    Returns:
        Image: processed image.
    """
    rgb_image = image.convert("RGB")
    image_array = np.array(rgb_image, dtype="float32") / 255.0

    # Soften highlights and lift shadows slightly.
    image_array = np.power(image_array, 0.92)
    image_array = image_array * 0.96 + 0.025

    red = image_array[:, :, 0] * 1.06 + 0.012
    green = image_array[:, :, 1] * 1.01 + 0.006
    blue = image_array[:, :, 2] * 0.94
    image_array = np.stack((red, green, blue), axis=2)

    luminance = (
        image_array[:, :, 0] * 0.299
        + image_array[:, :, 1] * 0.587
        + image_array[:, :, 2] * 0.114
    )
    saturation = 0.9
    image_array = luminance[:, :, np.newaxis] + (
        image_array - luminance[:, :, np.newaxis]
    ) * saturation

    image_array = np.clip(image_array, 0.0, 1.0)
    return Image.fromarray((image_array * 255).astype("uint8"))
