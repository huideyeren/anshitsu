import numpy as np
from PIL import Image, ImageChops


def _orthopanchromatic_grayscale(image: Image) -> Image:
    """
    Convert an image using a mild orthopanchromatic monochrome response.

    The response is less red-sensitive and more blue-sensitive than the
    standard luminance conversion, but not as extreme as an orthochromatic
    conversion.

    Parameters:
        image: Image

    Returns:
        Image: converted L mode image.
    """
    if image.mode == "L":
        return image

    rgb = np.array(image.convert("RGB"), dtype="float32")

    gamma = 2.2
    rgb_l = pow(rgb / 255.0, gamma)

    red = rgb_l[:, :, 0]
    green = rgb_l[:, :, 1]
    blue = rgb_l[:, :, 2]

    gray_l = 0.14 * red + 0.68 * green + 0.18 * blue
    gray = pow(gray_l, 1.0 / gamma) * 255

    return Image.fromarray(gray.astype("uint8"))


def _tone_curve(gray: np.ndarray) -> np.ndarray:
    """
    Apply a smooth monochrome tone curve with protected highlights.

    Parameters:
        gray: normalized grayscale image array

    Returns:
        np.ndarray: tone-adjusted normalized image array.
    """
    lifted = np.power(gray, 0.92)
    blacks = np.clip((lifted - 0.02) / 0.98, 0.0, 1.0)
    contrast = 3 * blacks**2 - 2 * blacks**3

    highlight_start = 0.78
    highlights = np.maximum(contrast - highlight_start, 0.0)
    compressed = highlights / (1.0 + highlights * 2.2)
    return np.minimum(contrast, highlight_start + compressed)


def _add_fine_grain(image: Image, amount: float) -> Image:
    """
    Add subtle monochrome grain to an L image.

    Parameters:
        image: L mode image
        amount: grain strength

    Returns:
        Image: grain-adjusted L image.
    """
    noise_image = Image.effect_noise(image.size, amount)
    table = [x * 2 for x in range(256)]
    return ImageChops.multiply(image, noise_image).point(table)


def roppongi(image: Image) -> Image:
    """
    Apply a smooth monochrome film preset inspired by Fujifilm ACROS.

    The preset converts the input with a mild orthopanchromatic response,
    compresses highlights, keeps blacks firm, and adds restrained fine grain.
    The public preset name avoids trademark use, but the intended rendering is
    the smooth modern monochrome look associated with ACROS.

    Parameters:
        image: Image

    Returns:
        Image: processed image in L mode.
    """
    monochrome = _orthopanchromatic_grayscale(image)
    gray = np.array(monochrome, dtype="float32") / 255.0
    toned = np.clip(_tone_curve(gray), 0.0, 1.0)
    processed = Image.fromarray((toned * 255).astype("uint8"))
    return _add_fine_grain(processed, 2.5)
