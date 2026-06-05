import importlib
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from anshitsu import image_io


class _DummyRaw:
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

    def import_module(name):
        if name == "rawpy":
            return dummy_rawpy
        return importlib.import_module(name)

    monkeypatch.setattr(image_io.importlib, "import_module", import_module)

    image = image_io.develop_raw_image(Path("input.dng"))

    assert image.mode == "RGB"
    assert image.size == (1, 1)
    assert image.getpixel((0, 0)) == (12, 34, 56)
    assert dummy_rawpy.path == "input.dng"
    assert dummy_rawpy.raw.kwargs["output_bps"] == 8
    assert dummy_rawpy.raw.kwargs["output_color"] is dummy_rawpy.ColorSpace.sRGB
    assert dummy_rawpy.raw.kwargs["use_auto_wb"] is True
    assert dummy_rawpy.raw.kwargs["highlight_mode"] is dummy_rawpy.HighlightMode.Blend


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
