# Anshitsu

[![Testing](https://github.com/huideyeren/anshitsu/actions/workflows/testing.yml/badge.svg)](https://github.com/huideyeren/anshitsu/actions/workflows/testing.yml)

[![codecov](https://codecov.io/gh/huideyeren/anshitsu/branch/main/graph/badge.svg?token=ZYRX8NBTLQ)](https://codecov.io/gh/huideyeren/anshitsu)

A tiny digital photographic utility.

"Anshitsu" means a darkroom in Japanese.

## Install

Run this command in an environment where Python 3.10 or higher is installed.

We have tested it on Windows, Mac, and Ubuntu on GitHub Actions, but we have not tested it on Macs with Apple Silicon, so please use it at your own risk on Macs with Apple Silicon.

``` shell
pip install anshitsu
```

## Usage

It is as described in the following help.

``` shell












NAME
    main.py - Process Runnner for Command Line Interface


SYNOPSIS
    main.py <flags>

DESCRIPTION
    This utility converts the colors of images such as photos.

    If you specify a directory path, it will convert
    the image files in the specified directory.
    If you specify a file path, it will convert the specified file.
    If you specify an option, the specified conversion will be performed.


    Tosaka mode is a mode that expresses the preference of
    Tosaka-senpai, a character in "Kyūkyoku Chōjin R",
    for "photos taken with Tri-X that look like they were
    burned onto No. 4 or No. 5 photographic paper".
    Only use floating-point numbers when using this mode;
    numbers around 2.4 will make it look right.

FLAGS
    --path=PATH
        Type: Optional[Optional]
        Default: None
        Directory or File Path. Defaults to None.
    -k, --keep_alpha=KEEP_ALPHA
        Type: bool
        Default: False
    --colorautoadjust=COLORAUTOADJUST
        Type: bool
        Default: False
        Use colorautoadjust algorithm. Defaults to False.
    --colorstretch=COLORSTRETCH
        Type: bool
        Default: False
        Use colorstretch algorithm. Defaults to False.
    -g, --grayscale=GRAYSCALE
    -g, --grayscale=GRAYSCALE
        Type: bool
        Default: False
        Convert to grayscale. Defaults to False.
    -i, --invert=INVERT
        Type: bool
        Default: False
        Invert color. Defaults to False.
    --color=COLOR
        Type: Optional[Optional]
        Default: None
        Fix color balance. Defaults to None.
    -b, --brightness=BRIGHTNESS
        Type: Optional[Optional]
        Default: None
        Fix brightness. Defaults to None.
    --sharpness=SHARPNESS
        Type: Optional[Optional]
        Default: None
        Fix sharpness. Defaults to None.
    --contrast=CONTRAST
        Type: Optional[Optional]
        Default: None
        Fix contrast. Defaults to None.
    -t, --tosaka=TOSAKA
        Type: Optional[Optional]
        Default: None
        Convert to grayscale with fix contrast. Defaults to None.
        Convert to grayscale with fix contrast. Defaults to None.
    --outputrgb=OUTPUTRGB
        Type: bool
        Default: False
        Outputs a monochrome image in RGB. Defaults to False.
    --sepia=SEPIA
        Type: bool
        Default: False
        Convert to RGB colored by sepia. Defaults to False.
    --cyanotype=CYANOTYPE
        Type: bool
        Default: False
        Convert to RGB like cyanotype. Defaults to False.
    -n, --noise=NOISE
        Type: Optional[Optional]
        Default: None
        Add Gaussian noise. Defaults to None.
    --overwrite=OVERWRITE
        Type: bool
        Default: False
        Default: False
    --overwrite=OVERWRITE
        Type: Optional[Optional]
        Convert to RGB like cyanotype. Defaults to False.
        Convert to RGB colored by sepia. Defaults to False.
        Default: None
    -t, --tosaka=TOSAKA
        Default: None
        Default: None
    --path=PATH
    burned onto No. 4 or No. 5 photographic paper".
NAME
    main.py - Process Runnner for Command Line Interface
    main.py - Process Runnner for Command Line Interface

SYNOPSIS
SYNOPSIS
    main.py <flags>


DESCRIPTION
DESCRIPTION
    This utility converts the colors of images such as photos.

    If you specify a directory path, it will convert
    If you specify a directory path, it will convert
    the image files in the specified directory.
    the image files in the specified directory.
    If you specify a file path, it will convert the specified file.
    If you specify an option, the specified conversion will be performed.

NAME
    main.py - Process Runnner for Command Line Interface

SYNOPSIS
    main.py <flags>

DESCRIPTION
    This utility converts the colors of images such as photos.

    If you specify a directory path, it will convert
    the image files in the specified directory.
    If you specify a file path, it will convert the specified file.
    If you specify an option, the specified conversion will be performed.

    Tosaka mode is a mode that expresses the preference of
    Tosaka-senpai, a character in "Kyūkyoku Chōjin R",
    for "photos taken with Tri-X that look like they were
    burned onto No. 4 or No. 5 photographic paper".
    Only use floating-point numbers when using this mode;
    numbers around 2.4 will make it look right.

POSITIONAL ARGUMENTS
    PATH
        Type: str
        Directory or File Path

FLAGS
    --path=PATH
        Type: Optional[Optional]
        Default: None
        Directory or File Path. Defaults to None.
    -k, --keep_alpha=KEEP_ALPHA
        Type: bool
        Default: False
    --colorautoadjust=COLORAUTOADJUST
        Type: bool
        Default: False
        Use colorautoadjust algorithm. Defaults to False.
    --colorstretch=COLORSTRETCH
        Type: bool
        Default: False
        Use colorstretch algorithm. Defaults to False.
    -g, --grayscale=GRAYSCALE
        Type: bool
        Default: False
        Convert to grayscale. Defaults to False.
    -i, --invert=INVERT
        Type: bool
        Default: False
        Invert color. Defaults to False.
    --color=COLOR
        Type: Optional[Optional]
        Default: None
        Fix color balance. Defaults to None.
    -b, --brightness=BRIGHTNESS
        Type: Optional[Optional]
        Default: None
        Fix brightness. Defaults to None.
    --sharpness=SHARPNESS
        Type: Optional[Optional]
        Default: None
        Fix sharpness. Defaults to None.
    --contrast=CONTRAST
        Type: Optional[Optional]
        Default: None
        Fix contrast. Defaults to None.
    -t, --tosaka=TOSAKA
        Type: Optional[Optional]
        Default: None
        Convert to grayscale with fix contrast. Defaults to None.
    --outputrgb=OUTPUTRGB
        Type: bool
        Default: False
        Outputs a monochrome image in RGB. Defaults to False.
    --sepia=SEPIA
        Type: bool
        Default: False
        Convert to RGB colored by sepia. Defaults to False.
    --cyanotype=CYANOTYPE
        Type: bool
        Default: False
        Convert to RGB like cyanotype. Defaults to False.
    -n, --noise=NOISE
        Type: Optional[Optional]
        Default: None
        Add Gaussian noise. Defaults to None.
    --overwrite=OVERWRITE
        Type: bool
        Default: False
        Overwrite original files. Defaults to False.
    -v, --version=VERSION
        Type: bool
        Default: False
        Show version. Defaults to False.
    -l, --line_drawing=LINE_DRAWING
        Type: bool
        Default: False
        Convert to like line drawing. Defaults to False.
    --posterize=POSTERIZE
        Type: Optional[Optional]
        Default: None
```

If a directory is specified in the path, an `out` directory will be created in the specified directory, and the converted JPEG and PNG images will be stored in PNG format.

If you specify a JPEG or PNG image file as the path, an `out` directory will be created in the directory where the image is stored, and the converted image will be stored in PNG format.

**Note:** If you specify a file in any other format in the path, be aware there is no error handling. The program will terminate abnormally.

## Algorithms

The following algorithms are available in this tool.

### RGBA to RGB Convert

Converts an image that contains Alpha, such as RGBA, to image data that does not contain Alpha.
Transparent areas will be filled with white.

This algorithm is performed on any image file.

### invert

Inverts the colors of an image using Pillow's built-in algorithm.

In the case of negative film, color conversion that takes into account the film base color is not performed, but we plan to follow up with a feature to be developed in the future.

### colorautoajust

We will use the "automatic color equalization" algorithm described in the following paper to apply color correction.

This process is more time consuming than the algorithm used in "colorstretch", but it can reproduce more natural colors.

(References)

A. Rizzi, C. Gatta and D. Marini, "A new algorithm for unsupervised global and local color correction.", Pattern Recognition Letters, vol. 24, no. 11, 2003.

### colorstretch

The "gray world" and "stretch" algorithms described in the following paper are combined to apply color correction.

This process is faster than the algorithm used in "colorautoajust".

(References)

D. Nikitenko, M. Wirth and K. Trudel, "Applicability Of White-Balancing Algorithms to Restoring Faded Colour Slides: An Empirical Evaluation.", Journal of Multimedia, vol. 3, no. 5, 2008.

### grayscale

Convert a color image to grayscale using the algorithm described in the following article.

[Python でグレースケール(grayscale)化](https://qiita.com/yoya/items/dba7c40b31f832e9bc2a#pilpillow-%E3%81%A7%E3%82%B0%E3%83%AC%E3%83%BC%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%AB%E5%8C%96-numpy-%E3%81%A7%E4%BD%8E%E8%BC%9D%E5%BA%A6%E5%AF%BE%E5%BF%9C)

Note: This article is written in Japanese.

### Tosaka mode

Tosaka mode is a mode that expresses the preference of Tosaka-senpai, a character in "Kyūkyoku Chōjin R", for "photos taken with Tri-X that look like they were burned onto No. 4 or No. 5 photographic paper".

Only use floating-point numbers when using this mode; numbers around 2.4 will make it look right.

When this mode is specified, color images will also be converted to grayscale.

### outputrgb

Outputs a monochrome image in RGB.

### noise

Add Gaussian noise.

To add noise, you need to specify a floating-point number; a value of about 10.0 will be just right.

## Special Thanks

We are using the following libraries.

[shunsukeaihara/colorcorrect](https://github.com/shunsukeaihara/colorcorrect)
