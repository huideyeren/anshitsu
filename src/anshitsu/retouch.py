from typing import Optional

import colorcorrect.algorithm as cca
import numpy as np
from colorcorrect.util import from_pil, to_pil
from PIL import Image, ImageEnhance, ImageOps


class Retouch:
    def __init__(
        self,
        image: Image,
        colorautoadjust: bool = False,
        colorstretch: bool = False,
        grayscale: bool = False,
        negative: bool = False,
        tosaka: Optional[float] = None,
    ) -> None:
        self.image = image
        self.colorautoadjust = colorautoadjust
        self.colorstretch = colorstretch
        self.grayscale = grayscale
        self.negative = negative
        self.tosaka = tosaka

    def process(self) -> Image:
        image = self.image

        if self.negative:
            image = self.__negative()

        if self.colorautoadjust:
            image = self.__colorautoadjust()

        if self.colorstretch:
            image = self.__colorstretch()

        image = self.__rgba_convert()

        if self.grayscale:
            image = self.__grayscale()

        if self.tosaka is not None:
            image = self.__tosaka()

        return image

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
        image = self.image
        if image.mode == "L" or image.mode == "LA":
            return image

        if image.mode != "RGB":
            image = image.convert("RGB")
        rgb = np.array(image, dtype="float32")

        rgbL = pow(rgb / 255.0, 2.2)
        r, g, b = rgbL[:, :, 0], rgbL[:, :, 1], rgbL[:, :, 2]
        grayL = 0.299 * r + 0.587 * g + 0.114 * b  # BT.601
        gray = pow(grayL, 1.0 / 2.2) * 255

        return Image.fromarray(gray.astype("uint8"))

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
        imageC = ImageEnhance.Contrast(self.image)
        return imageC.enhance(self.tosaka)

    def __rgba_convert(self) -> Image:
        """
        __rgba_convert [summary]

        Args:
            image (Image): base image.

        Returns:
            Image: processed image.
        """
        image = self.image
        if image.mode == "RGBA":
            image.load()
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
        return image
