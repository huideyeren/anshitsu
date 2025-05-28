import os

from anshitsu.process.processor import Processor
from PIL import Image

def test_sharpness_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, sharpness=1.2).process()
    assert image.mode == "RGB"


def test_sharpness_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, sharpness=1.2).process()
    assert image.mode == "L"


def test_sharpness_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, sharpness=1.2).process()
    assert image.mode == "RGB"


def test_sharpness_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, sharpness=1.2).process()
    assert image.mode == "L"