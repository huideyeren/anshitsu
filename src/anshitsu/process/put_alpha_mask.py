from PIL import Image


def put_alpha_mask(image: Image, alpha: Image) -> Image:
    """
    put_alpha_mask

    Adds or replaces the alpha layer in this image.

    Parameters:
        image: Image
        alpha: Image

    Returns:
        Image: Image having alpha layer.
    """
    return image.putalpha(alpha)
