import datetime
import glob
import os
import os.path
import re
from typing import Optional

import fire
import fire.core
from PIL import Image, UnidentifiedImageError

from anshitsu.__version__ import version as __version__
from anshitsu.process.processor import Processor


def cli(
    path: Optional[str] = None,
    keep_alpha: bool = False,
    colorautoadjust: bool = False,
    colorstretch: bool = False,
    grayscale: bool = False,
    orthochromatic: bool = False,
    invert: bool = False,
    color: Optional[float] = None,
    brightness: Optional[float] = None,
    sharpness: Optional[float] = None,
    contrast: Optional[float] = None,
    tosaka: Optional[float] = None,
    outputrgb: bool = False,
    sepia: bool = False,
    cyanotype: bool = False,
    rochester: bool = False,
    ashigara: bool = False,
    crossprocess: bool = False,
    apocalypse: bool = False,
    ultramarine: bool = False,
    roppongi: bool = False,
    classic: bool = False,
    noise: Optional[float] = None,
    overwrite: bool = False,
    version: bool = False,
    line_drawing: bool = False,
    posterize: Optional[int] = None,
    vignette: Optional[float] = None,
) -> str:
    """
    Process Runnner for Command Line Interface

    This utility converts the colors of images such as photos.

    If you specify a directory path, it will convert
    the image files in the specified directory.
    If you specify a file path, it will convert the specified file.
    If you specify an option, the specified conversion will be performed.

    Tosaka mode is named after Tosaka-senpai's "Tri-X de banzen"
    line from "Kyūkyoku Chōjin R". It aims for a grainy
    black-and-white photo look similar to Kodak Tri-X film.
    This mode converts the image to grayscale and adjusts contrast.
    Use floating-point numbers; values around 2.4 usually work well.

    Args:
        path (Optional[str], optional): Directory or file path. Defaults to None.
        keep_alpha (bool, optional): Keep the alpha channel. Defaults to False.
        colorautoadjust (bool, optional): Correct colors using Automatic Color Equalization. Defaults to False.
        colorstretch (bool, optional): Apply gray-world white balance and color stretching. Defaults to False.
        grayscale (bool, optional): Convert to grayscale. Defaults to False.
        orthochromatic (bool, optional): Convert to orthochromatic-style grayscale. Defaults to False.
        invert (bool, optional): Invert image colors. Defaults to False.
        color (Optional[float], optional): Adjust color. Defaults to None.
        brightness (Optional[float], optional): Adjust brightness. Defaults to None.
        sharpness (Optional[float], optional): Adjust sharpness. Defaults to None.
        contrast (Optional[float], optional): Adjust contrast. Defaults to None.
        tosaka (Optional[float], optional): Use Tosaka mode. Defaults to None.
        outputrgb (bool, optional): Convert a monochrome image to RGB. Defaults to False.
        sepia (bool, optional): Colorize a monochrome image with sepia tones. Defaults to False.
        cyanotype (bool, optional): Colorize a monochrome image with cyanotype-like Prussian blue. Defaults to False.
        rochester (bool, optional): Apply a warm color grade inspired by Kodak PORTRA 400. Defaults to False.
        ashigara (bool, optional): Apply a vivid color grade inspired by Fujifilm Velvia 100. Defaults to False.
        crossprocess (bool, optional): Apply a random cross-process-style color grade. Defaults to False.
        apocalypse (bool, optional): Apply a red-orange Velvia 100 cross-process preset. Defaults to False.
        ultramarine (bool, optional): Apply a blue-forward color grade inspired by Kodak Ultramax. Defaults to False.
        roppongi (bool, optional): Apply a smooth fine-grain monochrome preset. Defaults to False.
        classic (bool, optional): Apply a classic high-acutance monochrome preset. Defaults to False.
        noise (Optional[float], optional): Add Gaussian noise. Defaults to None.
        overwrite (bool, optional): Overwrite original files. Defaults to False.
        version (bool, optional): Show version. Defaults to False.
        line_drawing (bool, optional): Convert to a line drawing. Defaults to False.
        posterize (Optional[int], optional): Posterize the image. Defaults to None.
        vignette (Optional[float], optional): Darken image edges with a radial vignette. Defaults to None.

    Raises:
        fire.core.FireError: Error that occurs when the specified string is not a path.

    Returns:
        str: Message.
    """
    if version:
        return "Anshitsu version {}".format(__version__)
    if path is None:
        raise fire.core.FireError("No path specified!")
    types = ("*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG")
    files_glob = []
    return_path = ""
    now_s = datetime.datetime.now()
    output_dir = "anshitsu_out"
    original_dir = "anshitsu_orig"
    if os.path.isdir(path):
        for type in types:
            files_glob.extend(glob.glob(os.path.join(path, "**", type), recursive=True))
        files_glob = [file for file in files_glob if not file.__contains__(output_dir)]
        return_path = path

        if len(files_glob) == 0:
            raise fire.core.FireError(
                "There are no JPEG or PNG files in this directory."
            )
    elif os.path.isfile(path):
        files_glob.extend(glob.glob(path))
        return_path = os.path.abspath(os.path.join(path, os.pardir))
    else:
        raise fire.core.FireError("A non-path string was passed.")
    if overwrite is True:
        os.makedirs(os.path.join(return_path, original_dir))
    for i, file in enumerate(files_glob):
        try:
            image = Image.open(file)
        except UnidentifiedImageError as e:
            raise fire.core.FireError(e)
        exif = image.getexif()
        original_filename: str = os.path.split(file)[1]
        extension = original_filename.split(".")[-1]
        timestamp = now_s.strftime("%Y-%m-%d_%H-%M-%S")
        if overwrite is True:
            backup_filename = original_filename
            image.save(os.path.join(return_path, original_dir, backup_filename))
            filename = os.path.join(
                return_path, re.sub(r"\.[^.]+$", "", original_filename) + ".png"
            )
            remove_file_list = [".jpg", ".JPG", ".jpeg", ".JPEG", ".PNG"]
            for remove_file in remove_file_list:
                remove_file_name = (
                    re.sub(r"\.[^.]+$", "", original_filename) + remove_file
                )
                remove_file_path = os.path.join(return_path, remove_file_name)
                if os.path.isfile(remove_file_path):
                    os.remove(remove_file_path)
        else:
            filename = os.path.join(
                return_path,
                output_dir,
                re.sub(r"\.[^.]+$", "_", original_filename)
                + "_{0}_converted_at_{1}.png".format(extension, timestamp),
            )
        psr = Processor(
            image=image,
            keep_alpha=keep_alpha,
            colorautoadjust=colorautoadjust,
            colorstretch=colorstretch,
            grayscale=grayscale,
            orthochromatic=orthochromatic,
            color=color,
            contrast=contrast,
            brightness=brightness,
            sharpness=sharpness,
            invert=invert,
            tosaka=tosaka,
            outputrgb=outputrgb,
            cyanotype=cyanotype,
            sepia=sepia,
            rochester=rochester,
            ashigara=ashigara,
            crossprocess=crossprocess,
            apocalypse=apocalypse,
            ultramarine=ultramarine,
            roppongi=roppongi,
            classic=classic,
            noise=noise,
            line_drawing=line_drawing,
            posterize=posterize,
            vignette=vignette,
        )
        saved_image = psr.process()
        os.makedirs(os.path.join(return_path, output_dir), exist_ok=True)
        saved_image.save(
            filename,
            quality=100,  # Specify 100 as the highest image quality
            subsampling=0,
            exif=exif,
        )
        print("{0}/{1} done!".format((i + 1), str(len(files_glob))))

    return "The cli was completed successfully."
