from PIL import Image, ImageEnhance


def contrast(image: Image, contrast: float) -> Image:
    """
    contrast

    Fix contrast.

    Using in Tosaka mode.

    Tosaka mode is a mode that expresses the preference of
    Tosaka-senpai, a character in "Kyūkyoku Chōjin R",
    for "photos taken with Tri-X that look like they were
    burned onto No. 4 or No. 5 photographic paper".
    Only use floating-point numbers when using this mode;
    numbers around 2.4 will make it look right.

    Parameters:
        image: Image
        contrast: float

    Returns:
        Image: processed image.
    """
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)
    return image
