from typing import Optional

import numpy as np
from PIL import Image


def _soft_clip_highlights(image_array: np.ndarray) -> np.ndarray:
    """
    Compress highlights after the warm cross-process color shift.

    Parameters:
        image_array: normalized RGB image array

    Returns:
        np.ndarray: highlight-compressed normalized RGB image array.
    """
    highlight_start = 0.80
    compression = 2.6
    highlights = np.maximum(image_array - highlight_start, 0.0)
    compressed = highlights / (1.0 + highlights * compression)
    return np.minimum(image_array, highlight_start + compressed)


def apocalypse(image: Image, seed: Optional[int] = None) -> Image:
    """
    Apply a red-orange cross-process preset inspired by Velvia 100.

    This preset leans into the orange-to-red color cast often associated with
    cross-processing Velvia 100. It aims for a dramatic end-of-days palette:
    hot reds, heavy oranges, suppressed blues, strong saturation, and controlled
    highlights. The strength of the red shift varies slightly each time it runs;
    pass a seed to make the result reproducible for tests or comparisons.

    Parameters:
        image: Image
        seed: optional random seed

    Returns:
        Image: processed RGB image.
    """
    rng = np.random.default_rng(seed)
    red_shift = float(rng.uniform(0.75, 1.25))
    image_array = np.array(image.convert("RGB"), dtype="float32") / 255.0

    image_array = np.power(np.clip(image_array, 0.0, 1.0), (0.88, 0.98, 1.18))
    red = image_array[:, :, 0] * (1.18 + 0.10 * red_shift) + (
        0.035 + 0.020 * red_shift
    )
    green = image_array[:, :, 1] * (0.98 - 0.035 * red_shift) + 0.020
    blue = image_array[:, :, 2] * (0.78 - 0.12 * red_shift) - (
        0.010 + 0.010 * red_shift
    )
    image_array = np.stack((red, green, blue), axis=2)
    image_array = (image_array - 0.5) * (1.12 + 0.10 * red_shift) + 0.5

    luminance = (
        image_array[:, :, 0] * 0.299
        + image_array[:, :, 1] * 0.587
        + image_array[:, :, 2] * 0.114
    )
    image_array = luminance[:, :, np.newaxis] + (
        image_array - luminance[:, :, np.newaxis]
    ) * (1.18 + 0.20 * red_shift)

    image_array = _soft_clip_highlights(image_array)
    image_array = np.clip(image_array, 0.0, 0.992)
    return Image.fromarray((image_array * 255).astype("uint8"))
