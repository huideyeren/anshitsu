from typing import Optional

import colorcorrect.algorithm as cca
import numpy as np
from colorcorrect.util import from_pil, to_pil
from PIL import Image, ImageEnhance, ImageOps


class Retouch:
    """
    Retouch generator.
    """

    def __init__(self, image: Image) -> None:
        self.img = image

    def process(
        self,
        colorautoadjust: bool = False,
        colorstretch: bool = False,
        glayscale: bool = False,
        negative: bool = False,
        tosaka: Optional[float] = None,
    ) -> Image:
        """
        process
            processing images.

        Args:
            colorautoadjust (bool, optional): [description]. Defaults to False.
            colorstretch (bool, optional): [description]. Defaults to False.
            glayscale (bool, optional): [description]. Defaults to False.
            negative (bool, optional): [description]. Defaults to False.
            tosaka (Optional[float], optional): [description]. Defaults to None.

        Returns:
            Image: [description]
        """
        if negative:
            self.img = self.__negative(self.img)

        if colorautoadjust:
            self.img = self.__colorautoadjust(self.img)

        if colorstretch:
            self.img = self.__colorstretch(self.img)

        self.img = self.__rgba_convert(self.img)

        if glayscale:
            self.img = self.__glayscale(self.img)

        if tosaka is not None:
            self.img = self.__tosaka(self.img, tosaka)

        return self.img

    def __colorautoadjust(self, img: Image) -> Image:
        """
        __colorautoadjust


        Args:
            img (Image): base image.

        Returns:
            Image: processed image.
        """
        return to_pil(cca.automatic_color_equalization(from_pil(img)))

    def __colorstretch(self, img: Image) -> Image:
        """
        __colorstretch [summary]

        Args:
            img (Image): base image.

        Returns:
            Image: processed image.
        """
        return to_pil(cca.stretch(cca.grey_world(from_pil(img))))

    def __glayscale(self, img: Image) -> Image:
        """
        __glayscale [summary]

        Args:
            img (Image): base image.

        Returns:
            Image: processed image.
        """
        if img.mode == "L" or img.mode == "LA":
            return img

        if img.mode != "RGB":
            img = img.convert("RGB")
        rgb = np.array(img, dtype="float32")

        rgbL = pow(rgb / 255.0, 2.2)
        r, g, b = rgbL[:, :, 0], rgbL[:, :, 1], rgbL[:, :, 2]
        grayL = 0.299 * r + 0.587 * g + 0.114 * b  # BT.601
        gray = pow(grayL, 1.0 / 2.2) * 255

        return Image.fromarray(gray.astype("uint8"))

    def __negative(self, img: Image) -> Image:
        """
        __negative [summary]

        Args:
            img (Image): base image.

        Returns:
            Image: processed image.
        """
        return ImageOps.invert(img)

    def __tosaka(self, img: Image, tosaka: float) -> Image:
        """
        __tosaka [summary]

        Args:
            img (Image): base image.
            tosaka (float): [description]

        Returns:
            Image: processed image.
        """
        imgC = ImageEnhance.Contrast(img)
        return imgC.enhance(tosaka)

    def __rgba_convert(self, img: Image) -> Image:
        """
        __rgba_convert [summary]

        Args:
            img (Image): base image.

        Returns:
            Image: processed image.
        """
        if img.mode == "RGBA":
            img.load()
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
        return img
