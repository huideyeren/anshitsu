from PIL import Image, ImageOps


def posterize(image: Image, colors: int) -> Image:
    """
    Posterize an image.

    Parameters:
        image (Image): image to posterize
        colors (int): number of bits to keep for each color channel

    Returns:
        Image: posterized image
    """
    return ImageOps.posterize(image, colors)
