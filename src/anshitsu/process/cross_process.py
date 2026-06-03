from typing import Optional, Tuple

import numpy as np
from PIL import Image


def _select_profile(rng: np.random.Generator) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Select a cross-process color profile and add small random variation.

    Parameters:
        rng: random number generator

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]: gamma, scale, and bias arrays.
    """
    profiles = (
        (
            np.array((0.90, 1.05, 1.22), dtype="float32"),
            np.array((1.08, 1.16, 0.86), dtype="float32"),
            np.array((0.020, 0.030, -0.010), dtype="float32"),
        ),
        (
            np.array((1.12, 0.94, 0.88), dtype="float32"),
            np.array((1.18, 0.88, 1.12), dtype="float32"),
            np.array((0.025, -0.010, 0.020), dtype="float32"),
        ),
        (
            np.array((0.98, 1.02, 0.84), dtype="float32"),
            np.array((0.88, 1.10, 1.22), dtype="float32"),
            np.array((-0.005, 0.020, 0.030), dtype="float32"),
        ),
    )
    gamma, scale, bias = profiles[int(rng.integers(0, len(profiles)))]
    gamma = gamma + rng.normal(0.0, 0.035, 3).astype("float32")
    scale = scale + rng.normal(0.0, 0.035, 3).astype("float32")
    bias = bias + rng.normal(0.0, 0.010, 3).astype("float32")
    return gamma, scale, bias


def cross_process(image: Image, seed: Optional[int] = None) -> Image:
    """
    Apply a random cross-process-style color grade.

    Cross processing can produce unpredictable color shifts depending on film,
    chemistry, and exposure. This preset intentionally picks one of several
    color responses and adds small random variation each time it runs. Pass a
    seed to make the result reproducible for tests or comparisons.

    Parameters:
        image: Image
        seed: optional random seed

    Returns:
        Image: processed RGB image.
    """
    rng = np.random.default_rng(seed)
    gamma, scale, bias = _select_profile(rng)

    image_array = np.array(image.convert("RGB"), dtype="float32") / 255.0
    image_array = np.power(np.clip(image_array, 0.0, 1.0), gamma)
    image_array = image_array * scale + bias
    image_array = (image_array - 0.5) * float(rng.uniform(1.12, 1.28)) + 0.5

    luminance = (
        image_array[:, :, 0] * 0.299
        + image_array[:, :, 1] * 0.587
        + image_array[:, :, 2] * 0.114
    )
    saturation = float(rng.uniform(1.15, 1.35))
    image_array = luminance[:, :, np.newaxis] + (
        image_array - luminance[:, :, np.newaxis]
    ) * saturation

    image_array = np.clip(image_array, 0.0, 1.0)
    return Image.fromarray((image_array * 255).astype("uint8"))
