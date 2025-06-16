from PIL import Image, ImageFilter, ImageChops, ImageOps


def line_drawing(image: Image, invert: bool) -> Image:
    """
    line_drawing

    Paint like line drawing on an image.
    If invert is True, the image will be inverted.

    Parameters:
        image: Image
        invert: bool

    Returns:
        Image: processed image.
    """
    image = image.convert("L")
    img_filter = image.filter(ImageFilter.MaxFilter(5))
    line_draw = ImageChops.difference(image, img_filter)
    if not invert:
        line_draw = ImageOps.invert(line_draw)
    return line_draw
