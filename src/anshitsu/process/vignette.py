import numpy as np
from PIL import Image


def vignette(image: Image, vignette: float) -> Image:
    """
    Darken image edges with a radial vignette.

    Parameters:
        image: Image
        vignette: strength of the vignette effect

    Returns:
        Image: processed image.
    """
    if vignette <= 0:
        return image

    image_array = np.array(image, dtype="float32")
    height, width = image_array.shape[:2]
    y, x = np.ogrid[:height, :width]
    center_y = (height - 1) / 2
    center_x = (width - 1) / 2
    distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    max_distance = np.sqrt(center_x**2 + center_y**2)

    if max_distance == 0:
        return image

    normalized_distance = distance / max_distance
    mask = 1.0 - np.clip(vignette, 0.0, 1.0) * normalized_distance**2

    if image_array.ndim == 3:
        mask = mask[:, :, np.newaxis]

    image_array = image_array * mask
    return Image.fromarray(np.clip(image_array, 0, 255).astype("uint8"), image.mode)
