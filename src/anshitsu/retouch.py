from collections import namedtuple
from typing import Optional, Tuple

import colorcorrect.algorithm as cca
import numpy as np
from colorcorrect.util import from_pil, to_pil
from PIL import Image, ImageChops, ImageEnhance, ImageOps


class Retouch:
    """
    Perform retouching.

    Passing an image and options to the constructor will convert the specified image.
    """

    RGB_RED_VALUE: int = 255
    RGB_GREEN_VALUE: int = 255
    RGB_BLUE_VALUE: int = 255
    RGB_WHITE_COLOR: Tuple[int, int, int] = (
        RGB_RED_VALUE,
        RGB_GREEN_VALUE,
        RGB_BLUE_VALUE,
    )

    def __init__(
        self,
        image: Image,
        colorautoadjust: bool = False,
        colorstretch: bool = False,
        grayscale: bool = False,
        invert: bool = False,
        tosaka: Optional[float] = None,
        outputrgb: bool = False,
        noise: Optional[float] = None,
    ) -> None:
        """
        __init__ constructor.

        Args:
            image (Image): Image file.
            colorautoadjust (bool, optional): Use colorautoadjust algorithm. Defaults to False.
            colorstretch (bool, optional): Use colorstretch algorithm. Defaults to False.
            grayscale (bool, optional): Convert to grayscale. Defaults to False.
            invert (bool, optional): Invert color. Defaults to False.
            tosaka (Optional[float], optional): Use Tosaka mode. Defaults to None.
            outputrgb (bool, optional): Outputs a monochrome image in RGB. Defaults to False.
            noise (Optional[float], optional): Add Gaussian noise. Defaults to None.
        """
        self.image = image
        self.colorautoadjust = colorautoadjust
        self.colorstretch = colorstretch
        self.grayscale = grayscale
        self.invert = invert
        self.tosaka = tosaka
        self.output_rgb = outputrgb
        self.noise = noise

    def process(self) -> Image:
        self.image = self.__rgba_convert()

        if self.invert:
            self.image = self.__invert()

        if self.colorautoadjust:
            self.image = self.__colorautoadjust()

        if self.colorstretch:
            self.image = self.__colorstretch()

        if self.grayscale:
            self.image = self.__grayscale()

        if self.noise is not None:
            self.image = self.__noise()

        if self.tosaka is not None:
            self.image = self.__tosaka()

        if self.output_rgb:
            self.image = self.__output_rgb()

        return self.image

    def __colorautoadjust(self) -> Image:
        """
        __colorautoadjust

        Use colorautoadjust algorithm.

        Returns:
            Image: processed image.
        """
        if self.image.mode == "L":
            return self.image
        return to_pil(cca.automatic_color_equalization(from_pil(self.image)))

    def __colorstretch(self) -> Image:
        """
        __colorstretch

        Use colorstretch algorithm.

        Returns:
            Image: processed image.
        """
        if self.image.mode == "L":
            return self.image
        return to_pil(cca.stretch(cca.grey_world(from_pil(self.image))))

    def __noise(self) -> Image:
        """
        __noise

        Add Gaussian noise.
        To add noise, you need to specify floating-point numbers;
        a value of about 10.0 will be just right.

        Returns:
            Image: processed image.
        """
        table = [x * 2 for x in range(256)] * len(self.image.getbands())
        if self.image.mode == "RGB":
            noise_image = Image.effect_noise(
                (self.image.width, self.image.height), self.noise
            ).convert("RGB")
            self.image = ImageChops.multiply(self.image, noise_image).point(table)
        if self.image.mode == "L":
            noise_image = Image.effect_noise(
                (self.image.width, self.image.height), self.noise
            )
            self.image = ImageChops.multiply(self.image, noise_image).point(table)
        return self.image

    def __grayscale(self) -> Image:
        """
        __grayscale

        Converts to grayscale based on the luminance in the CIE XYZ color space.

        Returns:
            Image: processed image.
        """
        if self.image.mode == "L":
            return self.image

        rgb = np.array(self.image, dtype="float32")

        GAMMA = 2.2
        ColorMatrix = namedtuple("ColorMatrix", ("red", "green", "blue"))

        # Coefficients for luminance in CIE XYZ color space
        CIE_XYZ = ColorMatrix(0.2126, 0.7152, 0.0722)

        # Inverse Gamma Correction
        rgbL = pow(rgb / 255.0, GAMMA)

        # Extract RGB values
        r, g, b = rgbL[:, :, 0], rgbL[:, :, 1], rgbL[:, :, 2]

        # Convert to grayscale
        grayL = CIE_XYZ.red * r + CIE_XYZ.green * g + CIE_XYZ.blue * b

        # gamma correction
        gray = pow(grayL, 1.0 / GAMMA) * 255

        self.image = Image.fromarray(gray.astype("uint8"))

        return self.image

    def __invert(self) -> Image:
        """
        __invert

        Invert color.

        Returns:
            Image: processed image.
        """
        return ImageOps.invert(self.image)

    def __tosaka(self) -> Image:
        """
        __tosaka

        Use Tosaka mode.

        Tosaka mode is a mode that expresses the preference of
        Tosaka-senpai, a character in "Kyūkyoku Chōjin R",
        for "photos taken with Tri-X that look like they were
        burned onto No. 4 or No. 5 photographic paper".
        Only use floating-point numbers when using this mode;
        numbers around 2.4 will make it look right.

        Returns:
            Image: processed image.
        """
        if self.image.mode != "L":
            self.image = self.__grayscale()
        imageC = ImageEnhance.Contrast(self.image)
        self.image = imageC.enhance(self.tosaka)
        return self.image

    def __rgba_convert(self) -> Image:
        """
        __rgba_convert

        Converts image data that contains transparency to image data that does not contain transparency.

        Returns:
            Image: processed image.
        """
        if self.image.mode == "RGBA":
            self.image.load()
            background = Image.new("RGB", self.image.size, self.RGB_WHITE_COLOR)
            background.paste(self.image, mask=self.image.split()[3])
            self.image = background
        if self.image.mode == "LA":
            self.image.load()
            background = Image.new("L", self.image.size, 255)
            background.paste(self.image, mask=self.image.split()[1])
            self.image = background
        return self.image

    def __output_rgb(self) -> Image:
        """
        __output_rgb

        Outputs a monochrome image in RGB.

        Returns:
            Image: processed image.
        """
        if self.image.mode == "L":
            self.image = self.image.convert("RGB")
        return self.image
