import importlib
from pathlib import Path
from typing import Any, FrozenSet, Union

from PIL import Image

PathLike = Union[str, Path]

STANDARD_IMAGE_EXTENSIONS: FrozenSet[str] = frozenset(
    {
        ".jpg",
        ".jpeg",
        ".png",
    }
)
RAW_IMAGE_EXTENSIONS: FrozenSet[str] = frozenset(
    {
        ".3fr",
        ".arw",
        ".cr2",
        ".cr3",
        ".crw",
        ".dcr",
        ".dng",
        ".erf",
        ".iiq",
        ".kdc",
        ".mef",
        ".mos",
        ".mrw",
        ".nef",
        ".nrw",
        ".orf",
        ".pef",
        ".raf",
        ".raw",
        ".rw2",
        ".rwl",
        ".sr2",
        ".srf",
        ".x3f",
    }
)
SUPPORTED_IMAGE_EXTENSIONS: FrozenSet[str] = (
    STANDARD_IMAGE_EXTENSIONS | RAW_IMAGE_EXTENSIONS
)


class RawProcessingError(RuntimeError):
    """
    Error raised when a RAW image cannot be developed.
    """


def is_supported_image_file(path: PathLike) -> bool:
    """
    Return True when the path has an image extension supported by Anshitsu.
    """
    return Path(path).suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS


def is_raw_image_file(path: PathLike) -> bool:
    """
    Return True when the path has a RAW image extension.
    """
    return Path(path).suffix.lower() in RAW_IMAGE_EXTENSIONS


def open_image(path: PathLike) -> Image.Image:
    """
    Open a standard image with Pillow or develop a RAW image with rawpy.

    RAW files are converted to an 8-bit sRGB Pillow RGB image before they enter
    the normal processing pipeline.
    """
    if is_raw_image_file(path):
        return develop_raw_image(path)
    with Image.open(path) as image:
        image.load()
        return image.copy()


def develop_raw_image(path: PathLike) -> Image.Image:
    """
    Develop a RAW image with rawpy and return an RGB Pillow image.

    Automatic white balance and highlight blending are used so the result is a
    neutral starting point for the existing Anshitsu processing pipeline.
    """
    rawpy = _load_rawpy()
    try:
        with rawpy.imread(str(path)) as raw:
            rgb = raw.postprocess(
                output_bps=8,
                output_color=rawpy.ColorSpace.sRGB,
                use_auto_wb=True,
                highlight_mode=rawpy.HighlightMode.Blend,
            )
    except Exception as exc:
        raise RawProcessingError(f"Could not develop RAW image: {path}") from exc
    return Image.fromarray(rgb).convert("RGB")


def _load_rawpy() -> Any:
    try:
        return importlib.import_module("rawpy")
    except ImportError as exc:
        raise RawProcessingError(
            "RAW input requires rawpy. Install Anshitsu with RAW support or add rawpy."
        ) from exc
