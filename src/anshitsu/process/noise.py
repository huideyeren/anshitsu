from PIL import Image, ImageChops, ImageFilter


def _add_noise(channel: Image, amount: float, blur_radius: float = 0.0) -> Image:
    noise_image = Image.effect_noise(channel.size, amount)
    if blur_radius > 0:
        noise_image = noise_image.filter(ImageFilter.GaussianBlur(blur_radius))
    return ImageChops.add(channel, noise_image, offset=-128)


def noise(image: Image, noise: float) -> Image:
    """
    Add Gaussian noise.

    RGB images receive mostly luminance noise with weaker, softer chroma noise,
    which gives a more natural color-film grain than independent RGB noise.

    A value around 10.0 usually gives a natural amount of noise.

    Parameters:
        image: Image
        noise: float

    Returns:
        Image: processed image.
    """
    table = [x * 2 for x in range(256)] * len(image.getbands())
    if image.mode == "RGB":
        y, cb, cr = image.convert("YCbCr").split()
        chroma_noise = noise * 0.25
        image = Image.merge(
            "YCbCr",
            (
                _add_noise(y, noise),
                _add_noise(cb, chroma_noise, blur_radius=1.0),
                _add_noise(cr, chroma_noise, blur_radius=1.0),
            ),
        ).convert("RGB")
    if image.mode == "L":
        noise_image = Image.effect_noise((image.width, image.height), noise)
        image = ImageChops.multiply(image, noise_image).point(table)
    return image
