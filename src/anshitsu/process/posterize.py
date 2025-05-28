from PIL import Image, ImageOps


def posterize(image: Image, colors: int):
    """
    posterize

    Posterize an image.

    Parameters:
        image (Image): image to posterize
        colors (int): number of colors

    Returns:
        Image: posterized image
    """
    return ImageOps.posterize(image, colors)
