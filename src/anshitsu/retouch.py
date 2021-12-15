from typing import Optional

import colorcorrect.algorithm as cca
import numpy as np
from colorcorrect.util import from_pil, to_pil
from PIL import Image, ImageEnhance, ImageOps


class Retouch:
    """
    [summary]
    """

    def __init__(
        self,
        image: Image,
        colorautoadjust: bool = False,
        colorstretch: bool = False,
        grayscale: bool = False,
        negative: bool = False,
        tosaka: Optional[float] = None,
    ) -> None:
        """
        __init__ [summary]

        Args:
            image (Image): [description]
            colorautoadjust (bool, optional): [description]. Defaults to False.
            colorstretch (bool, optional): [description]. Defaults to False.
            grayscale (bool, optional): [description]. Defaults to False.
            negative (bool, optional): [description]. Defaults to False.
            tosaka (Optional[float], optional): [description]. Defaults to None.
        """
        self.image = image
        self.colorautoadjust = colorautoadjust
        self.colorstretch = colorstretch
        self.grayscale = grayscale
        self.negative = negative
        self.tosaka = tosaka

    def process(self) -> Image:
        if self.negative:
            self.image = self.__negative()

        if self.colorautoadjust:
            self.image = self.__colorautoadjust()

        if self.colorstretch:
            self.image = self.__colorstretch()

        self.image = self.__rgba_convert()

        if self.grayscale:
            self.image = self.__grayscale()

        if self.tosaka is not None:
            self.image = self.__tosaka()

        return self.image

    def __colorautoadjust(self) -> Image:
        """
        __colorautoadjust


        Args:
            image (Image): base image.

        Returns:
            Image: processed image.
        """
        return to_pil(cca.automatic_color_equalization(from_pil(self.image)))

    def __colorstretch(self) -> Image:
        """
        __colorstretch [summary]

        Args:
            image (Image): base image.

        Returns:
            Image: processed image.
        """
        return to_pil(cca.stretch(cca.grey_world(from_pil(self.image))))

    def __grayscale(self) -> Image:
        """
        __grayscale [summary]

        Args:
            image (Image): base image.

        Returns:
            Image: processed image.
        """
        if self.image.mode == "L" or self.image.mode == "LA":
            return self.image

        if self.image.mode != "RGB":
            self.image = self.image.convert("RGB")
        rgb = np.array(self.image, dtype="float32")

        rgbL = pow(rgb / 255.0, 2.2)
        r, g, b = rgbL[:, :, 0], rgbL[:, :, 1], rgbL[:, :, 2]
        grayL = 0.299 * r + 0.587 * g + 0.114 * b  # BT.601
        gray = pow(grayL, 1.0 / 2.2) * 255
        self.image = Image.fromarray(gray.astype("uint8"))

        return self.image

    def __negative(self) -> Image:
        """
        __negative [summary]

        Args:
            image (Image): base image.

        Returns:
            Image: processed image.
        """
        return ImageOps.invert(self.image)

    def __tosaka(self) -> Image:
        """
        __tosaka [summary]

        Args:
            image (Image): base image.
            tosaka (float): [description]

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
        __rgba_convert [summary]

        Args:
            image (Image): base image.

        Returns:
            Image: processed image.
        """
        if self.image.mode == "RGBA":
            self.image.load()
            background = Image.new("RGB", self.image.size, (255, 255, 255))
            background.paste(self.image, mask=self.image.split()[3])
            self.image = background
        if self.image.mode == "LA":
            self.image.load()
            background = Image.new("L", self.image.size, (255))
            background.paste(self.image, mask=self.image.split()[1])
            self.image = background
        return self.image
