import os

from PIL import Image

from anshitsu.process import _native_color
from anshitsu.process.processor import Processor


def test_colorautoadjust_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    ).resize((8, 8))
    image = Processor(image=image, colorautoadjust=True).process()
    assert image.mode == "RGB"


def test_colorautoadjust_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    ).resize((8, 8))
    image = Processor(image=image, colorautoadjust=True).process()
    assert image.mode == "L"


def test_colorautoadjust_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    ).resize((8, 8))
    image = Processor(image=image, colorautoadjust=True).process()
    assert image.mode == "RGB"


def test_colorautoadjust_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    ).resize((8, 8))
    image = Processor(image=image, colorautoadjust=True).process()
    assert image.mode == "L"


def test_colorautoadjust_uses_all_pixels_by_default(monkeypatch):
    captured = {}

    def native_color_auto_adjust(image, samples=None):
        captured["samples"] = samples
        return image.convert("RGB")

    monkeypatch.setattr(
        "anshitsu.process._native_color.automatic_color_equalization",
        native_color_auto_adjust,
    )
    image = Image.new("RGB", (3, 2), (128, 128, 128))

    Processor(image=image, colorautoadjust=True).process()

    assert captured["samples"] is None


def test_native_colorautoadjust_resolves_default_samples_to_all_pixels(monkeypatch):
    captured = {}

    class FakeLibrary:
        def anshitsu_ace_rgb(
            self, buffer, data_len, width, height, samples, slope, limit
        ):
            captured["samples"] = samples.value
            return 0

    monkeypatch.setattr(_native_color, "_load_library", lambda: FakeLibrary())
    image = Image.new("RGB", (3, 2), (128, 128, 128))

    _native_color.automatic_color_equalization(image)

    assert captured["samples"] == 6
