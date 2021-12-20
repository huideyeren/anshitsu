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
    --negative=NEGATIVE
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
