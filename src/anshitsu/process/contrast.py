from PIL import Image, ImageEnhance


def contrast(image: Image, contrast: float) -> Image:
    """
    Adjust image contrast.

    Used by Tosaka mode.

    Tosaka mode is named after Tosaka-senpai's "Tri-X de banzen"
    line from "Kyūkyoku Chōjin R". It aims for a grainy
    black-and-white photo look similar to Kodak Tri-X film.
    Values around 2.4 usually work well.

    Parameters:
        image: Image
        contrast: enhancement factor

    Returns:
        Image: processed image.
    """
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)
    return image
