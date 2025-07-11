import os

from PIL import Image

from anshitsu.process.processor import Processor


def test_colorstretch_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, colorstretch=True).process()
    assert image.mode == "RGB"


def test_colorstretch_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, colorstretch=True).process()
    assert image.mode == "L"


def test_colorstretch_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, colorstretch=True).process()
    assert image.mode == "RGB"


def test_colorstretch_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, colorstretch=True).process()
    assert image.mode == "L"
