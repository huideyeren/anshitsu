# Anshitsu

[![Testing](https://github.com/huideyeren/anshitsu/actions/workflows/testing.yml/badge.svg)](https://github.com/huideyeren/anshitsu/actions/workflows/testing.yml)

[![codecov](https://codecov.io/gh/huideyeren/anshitsu/branch/main/graph/badge.svg?token=ZYRX8NBTLQ)](https://codecov.io/gh/huideyeren/anshitsu)

A tiny digital photographic utility.

"Anshitsu" means a darkroom in Japanese.

## Usage

```
INFO: Showing help with the command 'anshitsu -- --help'.

NAME
    anshitsu - Process Runnner for Command Line Interface

SYNOPSIS
    anshitsu PATH <flags>

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
    --colorautoadjust=COLORAUTOADJUST
        Type: bool
        Default: False
        Use colorautoadjust algorithm. Defaults to False.
    --colorstretch=COLORSTRETCH
        Type: bool
        Default: False
        Use colorstretch algorithm. Defaults to False.
    --grayscale=GRAYSCALE
        Type: bool
        Default: False
        Convert to grayscale. Defaults to False.
    --invert=INVERT
        Type: bool
        Default: False
        Invert color. Defaults to False.
    --tosaka=TOSAKA
        Type: Optional[typing.Un...
        Default: None
        Use Tosaka mode. Defaults to None.

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```



## Algorithm

### RGBA to RGB Convert

Converts an image that contains Alpha, such as RGBA, to image data that does not contain Alpha.
Transparent areas will be filled with white.

### invert

Color inversion by pillow.

### colorautoajust

Using "automatic color equalization" algorithm.

(References)

A. Rizzi, C. Gatta and D. Marini, "A new algorithm for unsupervised global and local color correction.", Pattern Recognition Letters, vol. 24, no. 11, 2003.

### colorstretch

Using "stretch" algorithm after "gray world" algorithm.

(References)

D. Nikitenko, M. Wirth and K. Trudel, "Applicability Of White-Balancing Algorithms to Restoring Faded Colour Slides: An Empirical Evaluation.", Journal of Multimedia, vol. 3, no. 5, 2008.

### grayscale

I implemented it based on the method described in this article.

[Python でグレースケール(grayscale)化](https://qiita.com/yoya/items/dba7c40b31f832e9bc2a#pilpillow-%E3%81%A7%E3%82%B0%E3%83%AC%E3%83%BC%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%AB%E5%8C%96-numpy-%E3%81%A7%E4%BD%8E%E8%BC%9D%E5%BA%A6%E5%AF%BE%E5%BF%9C)

Note: This article is written in Japanese.

### Tosaka mode

Tosaka mode is a mode that expresses the preference of Tosaka-senpai, a character in "Kyūkyoku Chōjin R", for "photos taken with Tri-X that look like they were burned onto No. 4 or No. 5 photographic paper".

Only use floating-point numbers when using this mode; numbers around 2.4 will make it look right.

When this mode is specified, color images will also be converted to grayscale.

## Special Thanks

We are using the following libraries.

[shunsukeaihara/colorcorrect](https://github.com/shunsukeaihara/colorcorrect)
