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
    negative: bool = False,
    tosaka: Optional[float] = None,
) -> str:
    """
    process [summary]

    Args:
        path (str): [description]
        colorautoadjust (bool, optional): [description]. Defaults to False.
        colorstretch (bool, optional): [description]. Defaults to False.
        grayscale (bool, optional): [description]. Defaults to False.
        negative (bool, optional): [description]. Defaults to False.
        tosaka (Optional[float], optional): [description]. Defaults to None.

    Raises:
        fire.core.FireError: [description]

    Returns:
        str: [description]
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
        retouch = Retouch()
        image = retouch.process(
            image, colorautoadjust, colorstretch, grayscale, negative, tosaka
        )
        image.Image.save(
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


def main():
    """
    main [summary]
    """
    fire.Fire(process)


if __name__ == "__main__":
    main()
