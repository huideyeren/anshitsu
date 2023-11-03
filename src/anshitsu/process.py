import datetime
import glob
import os
import os.path
import re
from typing import Optional

import fire
import fire.core
from PIL import Image, UnidentifiedImageError

from anshitsu.retouch import Retouch
from anshitsu.__version__ import version as __version__


def process(
        path: Optional[str] = None,
        colorautoadjust: bool = False,
        colorstretch: bool = False,
        grayscale: bool = False,
        invert: bool = False,
        tosaka: Optional[float] = None,
        outputrgb: bool = False,
        noise: Optional[float] = None,
        overwrite: bool = False,
        version: bool = False,
) -> str:
    """
    Process Runnner for Command Line Interface

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

    Args:
        path (Optional[str], optional): Directory or File Path. Defaults to None.
        overwrite (bool, optional): Overwrite original files. Defaults to False.
        colorautoadjust (bool, optional): Use colorautoadjust algorithm. Defaults to False.
        colorstretch (bool, optional): Use colorstretch algorithm. Defaults to False.
        grayscale (bool, optional): Convert to grayscale. Defaults to False.
        invert (bool, optional): Invert color. Defaults to False.
        tosaka (Optional[float], optional): Use Tosaka mode. Defaults to None.
        outputrgb (bool, optional): Outputs a monochrome image in RGB. Defaults to False.
        noise (Optional[float], optional): Add Gaussian noise. Defaults to None.
        version (bool, optional): Show version. Defaults to False.

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
            files_glob.extend(glob.glob(os.path.join(path, '**', type), recursive=True))
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
            image.save(os.path.join(
                return_path,
                original_dir,
                backup_filename
            ))
            filename = os.path.join(return_path, re.sub(r"\.[^.]+$", "", original_filename) + ".png")
            remove_file_list = [".jpg", ".JPG", ".jpeg", ".JPEG", ".PNG"]
            for remove_file in remove_file_list:
                remove_file_name = re.sub(r"\.[^.]+$", "", original_filename) + remove_file
                remove_file_path = os.path.join(return_path, remove_file_name)
                if os.path.isfile(remove_file_path):
                    os.remove(remove_file_path)
        else:
            filename = os.path.join(
                return_path,
                output_dir,
                re.sub(r"\.[^.]+$", "_", original_filename)
                + "_{0}_converted_at_{1}.png".format(extension, timestamp))
        retouch = Retouch(
            image=image,
            colorautoadjust=colorautoadjust,
            colorstretch=colorstretch,
            grayscale=grayscale,
            invert=invert,
            tosaka=tosaka,
            outputrgb=outputrgb,
            noise=noise,
        )
        saved_image = retouch.process()
        os.makedirs(os.path.join(return_path, output_dir), exist_ok=True)
        saved_image.save(
            filename,
            quality=100,  # Specify 100 as the highest image quality
            subsampling=0,
            exif=exif,
        )
        print("{0}/{1} done!".format((i + 1), str(len(files_glob))))

    return "The process was completed successfully."
