import numpy as np
from PIL import Image


def _soft_clip_highlights(image_array: np.ndarray) -> np.ndarray:
    """
    Compress bright tones to keep the blue-leaning grade from clipping.

    Parameters:
        image_array: normalized RGB image array

    Returns:
        np.ndarray: highlight-compressed normalized RGB image array.
    """
    highlight_start = 0.80
    compression = 3.2
    highlights = np.maximum(image_array - highlight_start, 0.0)
    compressed = highlights / (1.0 + highlights * compression)
    return np.minimum(image_array, highlight_start + compressed)


def ultramarine(image: Image) -> Image:
    """
    Apply a blue-forward consumer color film grade inspired by Kodak Ultramax.

    The preset keeps a punchy snapshot-film look with stronger blues, slightly
    restrained reds, lively saturation, and protected highlights.

    Returns:
        Image: processed RGB image.
    """
    image_array = np.array(image.convert("RGB"), dtype="float32") / 255.0

    image_array = np.power(np.clip(image_array, 0.0, 1.0), (0.98, 0.96, 0.90))
    image_array = (image_array - 0.5) * 1.045 + 0.5

    red = image_array[:, :, 0] * 0.985 - 0.004
    green = image_array[:, :, 1] * 1.015 + 0.002
    blue = image_array[:, :, 2] * 1.09 + 0.018
    image_array = np.stack((red, green, blue), axis=2)

    luminance = (
        image_array[:, :, 0] * 0.299
        + image_array[:, :, 1] * 0.587
        + image_array[:, :, 2] * 0.114
    )
    saturation = 1.12
    image_array = (
        luminance[:, :, np.newaxis]
        + (image_array - luminance[:, :, np.newaxis]) * saturation
    )

    image_array = _soft_clip_highlights(image_array)
    image_array = np.clip(image_array, 0.0, 0.992)
    return Image.fromarray((image_array * 255).astype("uint8"))
