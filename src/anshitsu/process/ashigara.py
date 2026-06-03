import numpy as np
from PIL import Image


def _soft_clip_highlights(image_array: np.ndarray) -> np.ndarray:
    highlight_start = 0.78
    compression = 3.8
    highlights = np.maximum(image_array - highlight_start, 0.0)
    compressed = highlights / (1.0 + highlights * compression)
    return np.minimum(image_array, highlight_start + compressed)


def ashigara(image: Image) -> Image:
    """
    Apply a vivid, high-contrast color grade inspired by Fujifilm Velvia 100.

    Returns:
        Image: processed image.
    """
    rgb_image = image.convert("RGB")
    image_array = np.array(rgb_image, dtype="float32") / 255.0

    # Increase contrast with a restrained S-curve.
    image_array = 3 * image_array**2 - 2 * image_array**3
    image_array = (image_array - 0.5) * 1.035 + 0.5

    red = image_array[:, :, 0] * 1.025
    green = image_array[:, :, 1] * 1.02
    blue = image_array[:, :, 2] * 1.03
    image_array = np.stack((red, green, blue), axis=2)

    luminance = (
        image_array[:, :, 0] * 0.299
        + image_array[:, :, 1] * 0.587
        + image_array[:, :, 2] * 0.114
    )
    saturation = 1.14
    image_array = luminance[:, :, np.newaxis] + (
        image_array - luminance[:, :, np.newaxis]
    ) * saturation

    image_array = _soft_clip_highlights(image_array)
    image_array = np.clip(image_array, 0.0, 1.0)
    return Image.fromarray((image_array * 255).astype("uint8"))
