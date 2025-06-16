from typing import Optional, Tuple

from PIL import Image

from anshitsu.process.brightness import brightness
from anshitsu.process.color import color
from anshitsu.process.color_auto_adjust import color_auto_adjust
from anshitsu.process.color_stretch import color_stretch
from anshitsu.process.contrast import contrast
from anshitsu.process.cyanotype import cyanotype
from anshitsu.process.grayscale import grayscale
from anshitsu.process.invert import invert
from anshitsu.process.line_drawing import line_drawing
from anshitsu.process.noise import noise
from anshitsu.process.output_rgb import output_rgb
from anshitsu.process.posterize import posterize
from anshitsu.process.remove_alpha import remove_alpha
from anshitsu.process.sepia import sepia
from anshitsu.process.sharpness import sharpness
from anshitsu.process.create_alpha_mask import create_alpha_mask


class Processor:
    """
    Perform processing.

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
        line_drawing: bool = False,
        invert: bool = False,
        tosaka: Optional[float] = None,
        outputrgb: bool = False,
        noise: Optional[float] = None,
        color: Optional[float] = None,
        brightness: Optional[float] = None,
        sharpness: Optional[float] = None,
        contrast: Optional[float] = None,
        sepia: bool = False,
        cyanotype: bool = False,
        posterize: Optional[int] = None,
        keep_alpha: bool = False,
    ) -> None:
        """
        __init__ constructor.

        Args:
            image (Image): Image file.
            colorautoadjust (bool, optional): Use colorautoadjust algorithm. Defaults to False.
            colorstretch (bool, optional): Use colorstretch algorithm. Defaults to False.
            grayscale (bool, optional): Convert to grayscale. Defaults to False.
            invert (bool, optional): Invert color. Defaults to False.
            color (Optional[float], optional): Fix color balance. Defaults to None.
            brightness (Optional[float], optional): Fix brightness. Defaults to None.
            sharpness (Optional[float], optional): Fix sharpness. Defaults to None.
            contrast (Optional[float], optional): Fix contrast. Defaults to None.
            tosaka (Optional[float], optional): Use Tosaka mode. Defaults to None.
            outputrgb (bool, optional): Outputs a monochrome image in RGB. Defaults to False.
            noise (Optional[float], optional): Add Gaussian noise. Defaults to None.
            cyanotype (bool, optional): Convert to RGB like cyanotype. Defaults to False.
            sepia (bool, optional): Convert to RGB colored by sepia. Defaults to False.
            noise (Optional[float], optional): Add Gaussian noise. Defaults to None.
            line_drawing (bool, optional): Convert to like line drawing. Defaults to False.
            keep_alpha (bool, optional): Keep alpha mask. Defaults to False.
        """
        self.image = image
        self.keep_alpha = keep_alpha
        self.line_drawing = line_drawing
        self.colorautoadjust = colorautoadjust
        self.colorstretch = colorstretch
        self.grayscale = grayscale
        self.invert = invert
        self.color = color
        self.brightness = brightness
        self.sharpness = sharpness
        self.contrast = contrast
        if tosaka is not None:
            self.grayscale = True
            self.contrast = tosaka
        self.output_rgb = outputrgb
        self.noise = noise
        self.sepia = sepia
        self.cyanotype = cyanotype
        self.posterize = posterize

    def process(self) -> Image:
        if self.keep_alpha:
            alpha = create_alpha_mask(self.image)
        else:
            alpha = None

        self.image = remove_alpha(self.image)

        if self.invert:
            self.image = invert(self.image)

        if self.colorautoadjust:
            self.image = color_auto_adjust(self.image)

        if self.colorstretch:
            self.image = color_stretch(self.image)

        if self.color is not None:
            self.image = color(self.image, self.color)

        if self.brightness is not None:
            self.image = brightness(self.image, self.brightness)

        if self.sharpness is not None:
            self.image = sharpness(self.image, self.sharpness)

        if self.posterize is not None:
            self.image = posterize(self.image, self.posterize)

        if self.grayscale:
            self.image = grayscale(self.image)

        if self.contrast is not None:
            self.image = contrast(self.image, self.contrast)

        if self.line_drawing:
            self.image = line_drawing(self.image, self.invert)

        if self.noise is not None:
            self.image = noise(self.image, self.noise)

        if self.output_rgb:
            self.image = output_rgb(self.image)

        if self.sepia:
            self.image = sepia(self.image)

        if self.cyanotype:
            self.image = cyanotype(self.image)

        if alpha is not None:
            self.image.putalpha(alpha)

        return self.image
