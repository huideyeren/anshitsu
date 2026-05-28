from PIL import Image


def put_alpha_mask(image: Image, alpha: Image) -> None:
    """
    Add or replace the alpha channel in an image.

    Parameters:
        image: Image
        alpha: Image

    Returns:
        None: PIL mutates the image in place.
    """
    return image.putalpha(alpha)
