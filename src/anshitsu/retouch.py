from typing import Optional

import colorcorrect.algorithm as cca
import numpy as np
from colorcorrect.util import from_pil, to_pil
from PIL import Image, ImageEnhance, ImageOps


class Retouch:
    """
    Retouch generator.
    """

    def process(
        self,
        image: Image,
        colorautoadjust: bool,
        colorstretch: bool,
        grayscale: bool,
        negative: bool,
        tosaka: Optional[float] = None,
    ) -> Image:
        """
        process
            processing images.

        Args:
            image (Image): [description].
            colorautoadjust (bool, optional): [description]. Defaults to False.
            colorstretch (bool, optional): [description]. Defaults to False.
            grayscale (bool, optional): [description]. Defaults to False.
            negative (bool, optional): [description]. Defaults to False.
            tosaka (Optional[float], optional): [description]. Defaults to None.

        Returns:
            Image: [description]
        """
        if negative:
            image = self.__negative(image)

        if colorautoadjust:
            image = self.__colorautoadjust(image)

        if colorstretch:
            image = self.__colorstretch(image)

        image = self.__rgba_convert(image)

        if grayscale:
            image = self.__grayscale(image)

        if tosaka is not None:
            image = self.__tosaka(image, tosaka)

        return image

    def __colorautoadjust(self, image: Image) -> Image:
        """
        __colorautoadjust


        Args:
            image (Image): base image.

        Returns:
            Image: processed image.
        """
        return to_pil(cca.automatic_color_equalization(from_pil(image)))

    def __colorstretch(self, image: Image) -> Image:
        """
        __colorstretch [summary]

        Args:
            image (Image): base image.

        Returns:
            Image: processed image.
        """
        return to_pil(cca.stretch(cca.grey_world(from_pil(image))))

    def __grayscale(self, image: Image) -> Image:
        """
        __grayscale [summary]

        Args:
            image (Image): base image.

        Returns:
            Image: processed image.
        """
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

    def __negative(self, image: Image) -> Image:
        """
        __negative [summary]

        Args:
            image (Image): base image.

        Returns:
            Image: processed image.
        """
        return ImageOps.invert(image)

    def __tosaka(self, image: Image, tosaka: float) -> Image:
        """
        __tosaka [summary]

        Args:
            image (Image): base image.
            tosaka (float): [description]

        Returns:
            Image: processed image.
        """
        imageC = ImageEnhance.Contrast(image)
        return imageC.enhance(tosaka)

    def __rgba_convert(self, image: Image) -> Image:
        """
        __rgba_convert [summary]

        Args:
            image (Image): base image.

        Returns:
            Image: processed image.
        """
        if image.mode == "RGBA":
            image.load()
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
        return image
