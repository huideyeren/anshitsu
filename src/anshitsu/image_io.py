import importlib
from pathlib import Path
from typing import Any, FrozenSet, Mapping, Optional, Union

from PIL import ExifTags, Image
from PIL.PngImagePlugin import PngInfo, iTXt

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
PNG_TEXT_METADATA_KEY = "_anshitsu_png_text"


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
    the normal processing pipeline. JPEG and PNG EXIF is copied explicitly so
    it remains available after the source file is closed.
    """
    if is_raw_image_file(path):
        return develop_raw_image(path)
    with Image.open(path) as image:
        image.load()
        opened_image = image.copy()
        exif = get_exif_bytes(image)
        if exif is not None:
            opened_image.info["exif"] = exif
        png_text = getattr(image, "text", None)
        if png_text:
            # Image.copy() retains flattened info values but not the source
            # PNG's text mapping, which identifies the chunks to reconstruct.
            opened_image.info[PNG_TEXT_METADATA_KEY] = dict(png_text)
        return opened_image


def get_exif_bytes(image: Image.Image) -> Optional[bytes]:
    """
    Return an image's original EXIF packet when one is available.

    Keeping the packet unchanged avoids lossy re-encoding of non-standard but
    common metadata, such as UTF-8 text stored in an EXIF ASCII field. Images
    created in memory fall back to serializing their parsed EXIF mapping.
    """
    exif = image.info.get("exif")
    if isinstance(exif, bytes):
        return exif

    parsed_exif = image.getexif()
    return parsed_exif.tobytes() if parsed_exif else None


def create_png_metadata_info(
    text: Optional[Mapping[str, Any]], xmp: Optional[bytes]
) -> Optional[PngInfo]:
    """
    Build a PNG container that preserves text metadata and XMP.

    Ordinary tEXt and iTXt values retain comments, descriptions, application
    fields, and text-encoded IPTC profiles. XMP is reconstructed directly from
    bytes to avoid discarding unknown namespaces or altering application data.
    """
    if not text and not xmp:
        return None

    pnginfo = PngInfo()
    for key, value in (text or {}).items():
        if key == "XML:com.adobe.xmp" or not isinstance(value, str):
            continue
        if isinstance(value, iTXt):
            pnginfo.add_itxt(key, value, value.lang or "", value.tkey or "")
        else:
            # Pillow promotes non-Latin-1 strings to iTXt automatically.
            pnginfo.add_text(key, value)

    if xmp:
        keyword = b"XML:com.adobe.xmp"
        # The four null bytes encode an uncompressed iTXt chunk with empty
        # language and translated-keyword fields before the original packet.
        pnginfo.add(b"iTXt", keyword + b"\0\0\0\0\0" + xmp)
    return pnginfo


def develop_raw_image(path: PathLike) -> Image.Image:
    """
    Develop a RAW image with rawpy and return an RGB Pillow image.

    Automatic white balance and highlight blending are used so the result is a
    neutral starting point for the existing Anshitsu processing pipeline.
    """
    # rawpy develops pixels but does not transfer the RAW container's EXIF to
    # the resulting array. Read it separately so camera and lens information
    # can follow the developed image through the existing save pipeline.
    exif = _read_raw_exif(path)
    rawpy = _load_rawpy()
    try:
        with rawpy.imread(str(path)) as raw:
            lens = raw.lens
            rgb = raw.postprocess(
                output_bps=8,
                output_color=rawpy.ColorSpace.sRGB,
                use_auto_wb=True,
                highlight_mode=rawpy.HighlightMode.Blend,
            )
    except Exception as exc:
        raise RawProcessingError(f"Could not develop RAW image: {path}") from exc
    image = Image.fromarray(rgb).convert("RGB")
    exif = _add_rawpy_lens_exif(exif, lens)
    if exif is not None:
        image.info["exif"] = exif
    return image


def _read_raw_exif(path: PathLike) -> Optional[bytes]:
    """
    Return EXIF bytes from a RAW container when Pillow can read them.

    RAW pixel support varies by format, but many RAW containers expose their
    TIFF-based metadata to Pillow. Metadata extraction is best-effort because
    failure to parse optional EXIF must not prevent rawpy from developing an
    otherwise supported image.
    """
    try:
        with Image.open(path) as raw_image:
            exif = raw_image.getexif()
            exif_bytes = exif.tobytes()
            # An Exif object can contain a populated child IFD while its root
            # mapping is still empty, so its truth value alone is insufficient.
            return exif_bytes if exif_bytes != Image.Exif().tobytes() else None
    except (OSError, SyntaxError, ValueError):
        return None


def _add_rawpy_lens_exif(exif_bytes: Optional[bytes], lens: Any) -> Optional[bytes]:
    """
    Add LibRaw lens identity when the RAW EXIF does not already contain it.

    LibRaw understands lens metadata in some containers that Pillow cannot
    inspect, notably newer RAW formats. Existing EXIF values remain authoritative
    because they preserve the camera manufacturer's original representation.
    """
    if not lens.make and not lens.model:
        return exif_bytes

    exif = Image.Exif()
    if exif_bytes is not None:
        exif.load(exif_bytes)

    # Preserve the camera's original EXIF values and use LibRaw only to fill
    # gaps left by RAW formats that Pillow cannot inspect directly.
    exif_ifd = exif.get_ifd(ExifTags.IFD.Exif)
    if lens.make:
        exif_ifd.setdefault(ExifTags.Base.LensMake, lens.make)
    if lens.model:
        exif_ifd.setdefault(ExifTags.Base.LensModel, lens.model)
    return exif.tobytes()


def _load_rawpy() -> Any:
    try:
        return importlib.import_module("rawpy")
    except ImportError as exc:
        raise RawProcessingError(
            "RAW input requires rawpy. Install Anshitsu with RAW support or add rawpy."
        ) from exc
