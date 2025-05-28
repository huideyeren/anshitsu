import os

from anshitsu.process.processor import Processor
from PIL import Image


def test_line_drawing_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, line_drawing=True).process()
    assert image.mode == "L"


def test_line_drawing_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, line_drawing=True).process()
    assert image.mode == "L"


def test_line_drawing_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, line_drawing=True).process()
    assert image.mode == "L"


def test_line_drawing_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, line_drawing=True).process()
    assert image.mode == "L"

def test_inverted_line_drawing_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, line_drawing=True, invert=True).process()
    assert image.mode == "L"


def test_inverted_line_drawing_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, line_drawing=True, invert=True).process()
    assert image.mode == "L"


def test_inverted_line_drawing_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, line_drawing=True, invert=True).process()
    assert image.mode == "L"


def test_inverted_line_drawing_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, line_drawing=True, invert=True).process()
    assert image.mode == "L"
