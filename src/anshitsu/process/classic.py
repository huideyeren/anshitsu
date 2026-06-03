import numpy as np
from PIL import Image, ImageChops, ImageFilter

from anshitsu.process.grayscale import grayscale


def _classic_tone_curve(gray: np.ndarray) -> np.ndarray:
    """
    Apply a classic high-acutance monochrome tone curve.

    Parameters:
        gray: normalized grayscale image array

    Returns:
        np.ndarray: tone-adjusted normalized image array.
    """
    shadows = np.clip((gray - 0.015) / 0.985, 0.0, 1.0)
    contrast = 3 * shadows**2 - 2 * shadows**3
    contrast = (contrast - 0.5) * 1.12 + 0.5

    highlight_start = 0.86
    highlights = np.maximum(contrast - highlight_start, 0.0)
    compressed = highlights / (1.0 + highlights * 1.6)
    return np.minimum(contrast, highlight_start + compressed)


def _add_classic_grain(image: Image, amount: float) -> Image:
    """
    Add visible but restrained monochrome grain to an L image.

    Parameters:
        image: L mode image
        amount: grain strength

    Returns:
        Image: grain-adjusted L image.
    """
    noise_image = Image.effect_noise(image.size, amount)
    table = [x * 2 for x in range(256)]
    return ImageChops.multiply(image, noise_image).point(table)


def classic(image: Image) -> Image:
    """
    Apply a classic monochrome preset inspired by Kodak TRI-X in Rodinal.

    The preset converts the image to L mode, adds a firm but not extreme tone
    curve, protects the brightest highlights, adds visible fine grain, and
    applies mild sharpening. It is intended to be less aggressive than Tosaka
    mode while keeping the traditional high-acutance feel of TRI-X developed in
    Rodinal.

    Parameters:
        image: Image

    Returns:
        Image: processed image in L mode.
    """
    monochrome = grayscale(image)
    gray = np.array(monochrome, dtype="float32") / 255.0
    toned = np.clip(_classic_tone_curve(gray), 0.0, 1.0)
    processed = Image.fromarray((toned * 255).astype("uint8"))
    processed = _add_classic_grain(processed, 7.0)
    processed = processed.filter(ImageFilter.UnsharpMask(radius=1.0, percent=70, threshold=2))
    return processed.point(lambda value: min(value, 252))
