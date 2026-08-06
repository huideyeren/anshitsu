import datetime
import glob
import os
import os.path
import re
import shutil
from typing import Any, Optional, cast

import fire
import fire.core
from PIL import Image, UnidentifiedImageError

from anshitsu.__version__ import version as __version__
from anshitsu.image_io import (
    PNG_TEXT_METADATA_KEY,
    RawProcessingError,
    create_png_metadata_info,
    get_exif_bytes,
    is_supported_image_file,
    open_image,
)
from anshitsu.process.processor import Processor


def _prepare_image_for_jpeg(image: Image.Image) -> Image.Image:
    """
    Return an RGB image that JPEG can encode without losing transparent pixels.

    JPEG has no alpha channel, so transparent output is composited over white
    instead of letting Pillow silently discard alpha and expose black pixels.
    """
    if image.mode in ("RGBA", "LA") or "transparency" in image.info:
        rgba = image.convert("RGBA")
        # Pillow composites only equal-mode images; convert to RGB afterward
        # because JPEG has no alpha channel.
        flattened = Image.new("RGBA", rgba.size, "white")
        flattened.alpha_composite(rgba)
        return flattened.convert("RGB")
    return image.convert("RGB") if image.mode != "RGB" else image


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
    jpeg: bool = False,
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
        jpeg (bool, optional): Save the processed image as JPEG instead of PNG. Defaults to False.

    Raises:
        fire.core.FireError: Error that occurs when the specified string is not a path.

    Returns:
        str: Message.
    """
    if version:
        return "Anshitsu version {}".format(__version__)
    if path is None:
        raise fire.core.FireError("No path specified!")
    files_glob = []
    return_path = ""
    now_s = datetime.datetime.now()
    output_dir = "anshitsu_out"
    original_dir = "anshitsu_orig"
    if os.path.isdir(path):
        files_glob = [
            file
            for file in glob.glob(os.path.join(path, "**", "*"), recursive=True)
            if os.path.isfile(file)
            and is_supported_image_file(file)
            and not file.__contains__(output_dir)
        ]
        return_path = path

        if len(files_glob) == 0:
            raise fire.core.FireError(
                "There are no JPEG, PNG, or RAW files in this directory."
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
            image = open_image(file)
        except (UnidentifiedImageError, RawProcessingError) as e:
            raise fire.core.FireError(e)
        exif = get_exif_bytes(image)
        icc_profile = image.info.get("icc_profile")
        xmp = image.info.get("xmp")
        png_text = image.info.get(PNG_TEXT_METADATA_KEY)
        original_filename: str = os.path.split(file)[1]
        extension = original_filename.split(".")[-1]
        timestamp = now_s.strftime("%Y-%m-%d_%H-%M-%S")
        output_extension = "jpg" if jpeg else "png"
        if overwrite is True:
            backup_filename = original_filename
            shutil.copy2(file, os.path.join(return_path, original_dir, backup_filename))
            filename = os.path.join(
                return_path,
                re.sub(r"\.[^.]+$", "", original_filename) + "." + output_extension,
            )
            if os.path.abspath(file) != os.path.abspath(filename):
                os.remove(file)
        else:
            filename = os.path.join(
                return_path,
                output_dir,
                re.sub(r"\.[^.]+$", "_", original_filename)
                + "_{0}_converted_at_{1}.{2}".format(
                    extension, timestamp, output_extension
                ),
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
        # Processor always returns a Pillow image; its legacy annotation is
        # ambiguous to mypy because it imports the PIL module as ``Image``.
        saved_image = cast(Image.Image, psr.process())
        os.makedirs(os.path.join(return_path, output_dir), exist_ok=True)
        if jpeg:
            jpeg_save_options: dict[str, Any] = {
                "quality": 100,  # Specify 100 as the highest image quality
                "subsampling": 0,
            }
            # JPEG supports EXIF, ICC, and XMP but not PNG text chunks. Unlike
            # the PNG writer, Pillow's JPEG writer rejects ``None`` for EXIF.
            if exif is not None:
                jpeg_save_options["exif"] = exif
            if isinstance(icc_profile, bytes):
                jpeg_save_options["icc_profile"] = icc_profile
            if isinstance(xmp, bytes):
                jpeg_save_options["xmp"] = xmp
            _prepare_image_for_jpeg(saved_image).save(filename, **jpeg_save_options)
        else:
            saved_image.save(
                filename,
                quality=100,  # Specify 100 as the highest image quality
                subsampling=0,
                # Original bytes preserve nested IFDs and non-standard text without
                # a potentially lossy parse-and-reserialize cycle.
                exif=exif,
                icc_profile=icc_profile if isinstance(icc_profile, bytes) else None,
                pnginfo=create_png_metadata_info(
                    png_text if isinstance(png_text, dict) else None,
                    xmp if isinstance(xmp, bytes) else None,
                ),
            )
        print("{0}/{1} done!".format((i + 1), str(len(files_glob))))

    return "The cli was completed successfully."
