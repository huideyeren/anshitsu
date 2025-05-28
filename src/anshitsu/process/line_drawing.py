from PIL import Image, ImageFilter, ImageChops, ImageOps


def line_drawing(image: Image, invert: bool) -> Image:
    image = image.convert("L")
    img_filter = image.filter(ImageFilter.MaxFilter(5))
    line_draw = ImageChops.difference(image, img_filter)
    if not invert:
        line_draw = ImageOps.invert(line_draw)
    return line_draw
