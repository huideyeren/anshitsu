import importlib
from pathlib import Path

import numpy as np
import pytest
from PIL import ExifTags, Image, ImageCms

from anshitsu import image_io


class _DummyRaw:
    """Minimal rawpy image double with pixels and lens metadata."""

    class Lens:
        """Lens metadata exposed by the rawpy ``RawPy.lens`` property."""

        make = "LibRaw Lens Maker"
        model = "LibRaw 50mm F1.8"

    lens = Lens()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None

    def postprocess(self, **kwargs):
        self.kwargs = kwargs
        return np.array([[[12, 34, 56]]], dtype=np.uint8)


class _DummyRawPy:
    class ColorSpace:
        sRGB = object()

    class HighlightMode:
        Blend = object()

    def __init__(self):
        self.raw = _DummyRaw()
        self.path = None

    def imread(self, path):
        self.path = path
        return self.raw


class _FailingRawPy(_DummyRawPy):
    def imread(self, path):
        raise ValueError(f"cannot read {path}")


def test_is_supported_image_file_detects_standard_and_raw_extensions():
    assert image_io.is_supported_image_file("photo.JPG")
    assert image_io.is_supported_image_file("photo.dng")
    assert image_io.is_supported_image_file("photo.CR3")
    assert not image_io.is_supported_image_file("notes.txt")


def test_is_raw_image_file_detects_raw_extensions():
    assert image_io.is_raw_image_file("photo.pef")
    assert image_io.is_raw_image_file("photo.DNG")
    assert not image_io.is_raw_image_file("photo.png")


def test_open_image_uses_pillow_for_standard_images(tmp_path):
    path = tmp_path / "input.png"
    Image.new("RGB", (1, 1), (1, 2, 3)).save(path)

    image = image_io.open_image(path)

    assert image.mode == "RGB"
    assert image.getpixel((0, 0)) == (1, 2, 3)


@pytest.mark.parametrize("extension", ["jpg", "png"])
def test_open_image_preserves_standard_image_exif(tmp_path, extension):
    """JPEG and PNG metadata must survive after the source image is closed."""
    path = tmp_path / f"input.{extension}"
    exif = Image.Exif()
    exif_ifd = exif.get_ifd(ExifTags.IFD.Exif)
    exif_ifd[ExifTags.Base.LensMake] = "Example Lens Maker"
    exif_ifd[ExifTags.Base.LensModel] = "Example 35mm F2"
    icc_profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    xmp = b'<x:xmpmeta xmlns:x="adobe:ns:meta/">metadata</x:xmpmeta>'
    save_options = {"exif": exif.tobytes(), "icc_profile": icc_profile}
    if extension == "jpg":
        save_options["xmp"] = xmp
    else:
        save_options["pnginfo"] = image_io.create_png_metadata_info(
            {"Comment": "日本語の説明", "Make": "Example Application"}, xmp
        )
    Image.new("RGB", (1, 1), (1, 2, 3)).save(path, **save_options)

    image = image_io.open_image(path)

    saved_exif_ifd = image.getexif().get_ifd(ExifTags.IFD.Exif)
    assert saved_exif_ifd[ExifTags.Base.LensMake] == "Example Lens Maker"
    assert saved_exif_ifd[ExifTags.Base.LensModel] == "Example 35mm F2"
    assert image.info["icc_profile"] == icc_profile
    assert image.info["xmp"] == xmp
    if extension == "png":
        png_text = image.info[image_io.PNG_TEXT_METADATA_KEY]
        assert png_text["Comment"] == "日本語の説明"
        assert png_text["Make"] == "Example Application"


def test_create_png_metadata_info_returns_none_without_metadata():
    """Absent text and XMP must not create an empty PNG metadata container."""
    assert image_io.create_png_metadata_info(None, None) is None
    assert image_io.create_png_metadata_info({}, b"") is None


def test_get_exif_bytes_prefers_original_packet():
    """Original EXIF bytes must take priority over parsed metadata."""
    image = Image.new("RGB", (1, 1))
    image.info["exif"] = b"original exif packet"

    assert image_io.get_exif_bytes(image) == b"original exif packet"


def test_open_image_develops_raw_images(monkeypatch):
    def develop_raw_image(path):
        assert path == "input.cr2"
        return Image.new("RGB", (1, 1), (4, 5, 6))

    monkeypatch.setattr(image_io, "develop_raw_image", develop_raw_image)

    image = image_io.open_image("input.cr2")

    assert image.mode == "RGB"
    assert image.getpixel((0, 0)) == (4, 5, 6)


def test_develop_raw_image_uses_rawpy(monkeypatch):
    dummy_rawpy = _DummyRawPy()
    source_exif = Image.Exif()
    source_exif.get_ifd(ExifTags.IFD.Exif)[
        ExifTags.Base.LensMake
    ] = "Example Lens Maker"

    class _RawMetadata:
        """Pillow image double that exposes EXIF without decoding RAW pixels."""

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return None

        def getexif(self):
            return source_exif

    def import_module(name):
        if name == "rawpy":
            return dummy_rawpy
        return importlib.import_module(name)

    monkeypatch.setattr(image_io.importlib, "import_module", import_module)
    monkeypatch.setattr(image_io.Image, "open", lambda path: _RawMetadata())

    image = image_io.develop_raw_image(Path("input.dng"))

    assert image.mode == "RGB"
    assert image.size == (1, 1)
    assert image.getpixel((0, 0)) == (12, 34, 56)
    exif_ifd = image.getexif().get_ifd(ExifTags.IFD.Exif)
    assert exif_ifd[ExifTags.Base.LensMake] == "Example Lens Maker"
    assert exif_ifd[ExifTags.Base.LensModel] == "LibRaw 50mm F1.8"
    assert dummy_rawpy.path == "input.dng"
    assert dummy_rawpy.raw.kwargs["output_bps"] == 8
    assert dummy_rawpy.raw.kwargs["output_color"] is dummy_rawpy.ColorSpace.sRGB
    assert dummy_rawpy.raw.kwargs["use_auto_wb"] is True
    assert dummy_rawpy.raw.kwargs["highlight_mode"] is dummy_rawpy.HighlightMode.Blend


def test_develop_raw_image_ignores_unreadable_exif(monkeypatch):
    dummy_rawpy = _DummyRawPy()

    def import_module(name):
        if name == "rawpy":
            return dummy_rawpy
        return importlib.import_module(name)

    def unreadable_raw(path):
        raise Image.UnidentifiedImageError(path)

    monkeypatch.setattr(image_io.importlib, "import_module", import_module)
    monkeypatch.setattr(image_io.Image, "open", unreadable_raw)

    image = image_io.develop_raw_image("input.cr3")

    assert image.getpixel((0, 0)) == (12, 34, 56)
    exif_ifd = image.getexif().get_ifd(ExifTags.IFD.Exif)
    assert exif_ifd[ExifTags.Base.LensMake] == "LibRaw Lens Maker"
    assert exif_ifd[ExifTags.Base.LensModel] == "LibRaw 50mm F1.8"


def test_develop_raw_image_reports_rawpy_processing_errors(monkeypatch):
    failing_rawpy = _FailingRawPy()

    def import_module(name):
        if name == "rawpy":
            return failing_rawpy
        return importlib.import_module(name)

    monkeypatch.setattr(image_io.importlib, "import_module", import_module)

    with pytest.raises(
        image_io.RawProcessingError, match="Could not develop RAW image"
    ):
        image_io.develop_raw_image("input.cr2")


def test_develop_raw_image_reports_missing_rawpy(monkeypatch):
    def import_module(name):
        raise ImportError(name)

    monkeypatch.setattr(image_io.importlib, "import_module", import_module)

    with pytest.raises(image_io.RawProcessingError, match="RAW input requires rawpy"):
        image_io.develop_raw_image("input.dng")
