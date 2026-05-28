from typing import Optional, Tuple

from PIL import Image

from anshitsu.process.ashigara import ashigara
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
from anshitsu.process.rochester import rochester
from anshitsu.process.sepia import sepia
from anshitsu.process.sharpness import sharpness
from anshitsu.process.create_alpha_mask import create_alpha_mask
from anshitsu.process.vignette import vignette


class Processor:
    """
    Apply the requested image processing operations.
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
        rochester: bool = False,
        ashigara: bool = False,
        posterize: Optional[int] = None,
        vignette: Optional[float] = None,
        keep_alpha: bool = False,
    ) -> None:
        """
        Initialize a processor for an image and processing options.

        Args:
            image (Image): Image file.
            colorautoadjust (bool, optional): Correct colors using Automatic Color Equalization. Defaults to False.
            colorstretch (bool, optional): Apply gray-world white balance and color stretching. Defaults to False.
            grayscale (bool, optional): Convert to grayscale. Defaults to False.
            line_drawing (bool, optional): Convert to a line drawing. Defaults to False.
            invert (bool, optional): Invert image colors. Defaults to False.
            tosaka (Optional[float], optional): Use Tosaka mode. Defaults to None.
            outputrgb (bool, optional): Convert a monochrome image to RGB. Defaults to False.
            noise (Optional[float], optional): Add Gaussian noise. Defaults to None.
            color (Optional[float], optional): Adjust color. Defaults to None.
            brightness (Optional[float], optional): Adjust brightness. Defaults to None.
            sharpness (Optional[float], optional): Adjust sharpness. Defaults to None.
            contrast (Optional[float], optional): Adjust contrast. Defaults to None.
            sepia (bool, optional): Colorize a monochrome image with sepia tones. Defaults to False.
            cyanotype (bool, optional): Colorize a monochrome image with cyanotype-like Prussian blue. Defaults to False.
            rochester (bool, optional): Apply a warm color grade inspired by Kodak PORTRA 400. Defaults to False.
            ashigara (bool, optional): Apply a vivid color grade inspired by Fujifilm Velvia 100. Defaults to False.
            posterize (Optional[int], optional): Posterize the image. Defaults to None.
            vignette (Optional[float], optional): Darken image edges with a radial vignette. Defaults to None.
            keep_alpha (bool, optional): Keep the alpha channel. Defaults to False.
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
        self.rochester = rochester
        self.ashigara = ashigara
        self.posterize = posterize
        self.vignette = vignette

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

        if self.rochester:
            self.image = rochester(self.image)

        if self.ashigara:
            self.image = ashigara(self.image)

        if self.vignette is not None:
            self.image = vignette(self.image, self.vignette)

        if alpha is not None:
            self.image.putalpha(alpha)

        return self.image
