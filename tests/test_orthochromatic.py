import os

from PIL import Image

from anshitsu.process.orthochromatic import orthochromatic
from anshitsu.process.processor import Processor


def test_orthochromatic_darkens_red_more_than_blue():
    red = Image.new("RGB", (1, 1), (255, 0, 0))
    blue = Image.new("RGB", (1, 1), (0, 0, 255))

    red_gray = orthochromatic(red)
    blue_gray = orthochromatic(blue)

    assert red_gray.mode == "L"
    assert blue_gray.mode == "L"
    assert red_gray.getpixel((0, 0)) < blue_gray.getpixel((0, 0))


def test_orthochromatic_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, orthochromatic=True).process()
    assert image.mode == "L"


def test_orthochromatic_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, orthochromatic=True).process()
    assert image.mode == "L"


def test_orthochromatic_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, orthochromatic=True).process()
    assert image.mode == "L"


def test_orthochromatic_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, orthochromatic=True).process()
    assert image.mode == "L"
