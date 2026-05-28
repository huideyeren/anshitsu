import os

from PIL import Image

from anshitsu.process.processor import Processor
from anshitsu.process.rochester import rochester


def test_rochester_changes_rgb_color():
    image = Image.new("RGB", (1, 1), (120, 120, 120))
    image = rochester(image)

    assert image.getpixel((0, 0)) != (120, 120, 120)


def test_rochester_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, rochester=True).process()
    assert image.mode == "RGB"


def test_rochester_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, rochester=True).process()
    assert image.mode == "RGB"


def test_rochester_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, rochester=True).process()
    assert image.mode == "RGB"


def test_rochester_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, rochester=True).process()
    assert image.mode == "RGB"
