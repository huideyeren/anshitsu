import os

from PIL import Image

from anshitsu.process.ashigara import ashigara
from anshitsu.process.processor import Processor


def test_ashigara_changes_rgb_color():
    image = Image.new("RGB", (1, 1), (120, 120, 120))
    image = ashigara(image)

    assert image.getpixel((0, 0)) != (120, 120, 120)


def test_ashigara_preserves_highlight_detail():
    image = Image.new("RGB", (1, 1), (245, 245, 245))
    image = ashigara(image)

    assert max(image.getpixel((0, 0))) < 255


def test_ashigara_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, ashigara=True).process()
    assert image.mode == "RGB"


def test_ashigara_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, ashigara=True).process()
    assert image.mode == "RGB"


def test_ashigara_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, ashigara=True).process()
    assert image.mode == "RGB"


def test_ashigara_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, ashigara=True).process()
    assert image.mode == "RGB"
