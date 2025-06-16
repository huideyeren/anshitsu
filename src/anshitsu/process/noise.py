from PIL import Image, ImageChops


def noise(image: Image, noise: float) -> Image:
    """
    noise

    Add Gaussian noise.
    To add noise, you need to specify floating-point numbers;
    a value of about 10.0 will be just right.

    Parameters:
        image: Image
        noise: float

    Returns:
        Image: processed image.
    """
    table = [x * 2 for x in range(256)] * len(image.getbands())
    if image.mode == "RGB":
        noise_image = Image.effect_noise((image.width, image.height), noise).convert(
            "RGB"
        )
        image = ImageChops.multiply(image, noise_image).point(table)
    if image.mode == "L":
        noise_image = Image.effect_noise((image.width, image.height), noise)
        image = ImageChops.multiply(image, noise_image).point(table)
    return image
