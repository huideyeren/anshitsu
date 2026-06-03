import os

from PIL import Image

from anshitsu.process.classic import classic
from anshitsu.process.processor import Processor


def test_classic_returns_monochrome_image():
    image = Image.new("RGB", (8, 8), (128, 128, 128))
    processed = classic(image)

    assert processed.mode == "L"


def test_classic_keeps_highlights_below_white_clip():
    image = Image.new("RGB", (8, 8), (245, 245, 245))
    processed = classic(image)

    assert max(processed.getdata()) < 255


def test_classic_has_firmer_blacks_than_neutral_gray():
    dark = Image.new("RGB", (8, 8), (48, 48, 48))
    middle = Image.new("RGB", (8, 8), (128, 128, 128))

    dark_processed = classic(dark)
    middle_processed = classic(middle)

    assert min(dark_processed.getdata()) < min(middle_processed.getdata())


def test_classic_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, classic=True).process()
    assert image.mode == "L"


def test_classic_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, classic=True).process()
    assert image.mode == "L"


def test_classic_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, classic=True).process()
    assert image.mode == "L"


def test_classic_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, classic=True).process()
    assert image.mode == "L"
