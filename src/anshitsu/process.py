import datetime
import glob
import os
import os.path
from typing import Optional

import fire
import fire.core
from PIL import Image

from anshitsu.retouch import Retouch


def process(
    path: str,
    colorautoadjust: bool = False,
    colorstretch: bool = False,
    grayscale: bool = False,
    invert: bool = False,
    tosaka: Optional[float] = None,
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
        path (str): Directory or File Path
        colorautoadjust (bool, optional): Use colorautoadjust algorithm. Defaults to False.
        colorstretch (bool, optional): Use colorstretch algorithm. Defaults to False.
        grayscale (bool, optional): Convert to grayscale. Defaults to False.
        invert (bool, optional): Invert color. Defaults to False.
        tosaka (Optional[float], optional): Use Tosaka mode. Defaults to None.

    Raises:
        fire.core.FireError: Error that occurs when the specified string is not a path.

    Returns:
        str: Message.
    """
    types = ("*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG")
    files_glob = []
    return_path = ""
    now_s = datetime.datetime.now()
    if os.path.isdir(path):
        for files in types:
            files_glob.extend(
                glob.glob(
                    os.path.join(path, "**", files),
                    recursive=True,
                )
            )
        return_path = path
    elif os.path.isfile(path):
        files_glob.extend(glob.glob(path))
        return_path = os.path.abspath(os.path.join(path, os.pardir))
    else:
        raise fire.core.FireError("A non-path string was passed.")
    for i, file in enumerate(files_glob):
        image = Image.open(file)
        retouch = Retouch(
            image=image,
            colorautoadjust=colorautoadjust,
            colorstretch=colorstretch,
            grayscale=grayscale,
            invert=invert,
            tosaka=tosaka,
        )
        saved_image = retouch.process()
        os.makedirs(os.path.join(return_path, "out"), exist_ok=True)
        saved_image.save(
            os.path.join(
                return_path,
                "out",
                "{0}_{1}.jpg".format(now_s.strftime("%Y-%m-%d_%H-%M-%S"), (i + 1)),
            ),
            quality=100,
            subsampling=0,
        )
        print("{0}/{1} done!".format((i + 1), str(len(files_glob))))

    return "The process was completed successfully."
