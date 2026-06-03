import os

from PIL import Image

from anshitsu.process.processor import Processor
from anshitsu.process.ultramarine import ultramarine


def test_ultramarine_returns_rgb_image():
    image = Image.new("RGB", (2, 2), (120, 130, 140))
    processed = ultramarine(image)

    assert processed.mode == "RGB"


def test_ultramarine_shifts_neutral_toward_blue():
    image = Image.new("RGB", (2, 2), (120, 120, 120))
    processed = ultramarine(image)
    red, green, blue = processed.getpixel((0, 0))

    assert blue > green > red


def test_ultramarine_preserves_highlight_detail():
    image = Image.new("RGB", (2, 2), (245, 245, 245))
    processed = ultramarine(image)

    assert max(processed.getpixel((0, 0))) < 255


def test_ultramarine_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, ultramarine=True).process()
    assert image.mode == "RGB"


def test_ultramarine_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, ultramarine=True).process()
    assert image.mode == "RGB"


def test_ultramarine_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, ultramarine=True).process()
    assert image.mode == "RGB"


def test_ultramarine_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, ultramarine=True).process()
    assert image.mode == "RGB"
