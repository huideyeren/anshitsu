import os

from PIL import Image

from anshitsu.process.processor import Processor


def test_line_drawing_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, line_drawing=True).process()
    image.show()
    assert image.mode == "L"


def test_line_drawing_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, line_drawing=True).process()
    image.show()
    assert image.mode == "L"


def test_line_drawing_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, line_drawing=True).process()
    image.show()
    assert image.mode == "L"


def test_line_drawing_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, line_drawing=True).process()
    image.show()
    assert image.mode == "L"


def test_inverted_line_drawing_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, line_drawing=True, invert=True).process()
    image.show()
    assert image.mode == "L"


def test_inverted_line_drawing_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, line_drawing=True, invert=True).process()
    image.show()
    assert image.mode == "L"


def test_inverted_line_drawing_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, line_drawing=True, invert=True).process()
    image.show()
    assert image.mode == "L"


def test_inverted_line_drawing_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, line_drawing=True, invert=True).process()
    image.show()
    assert image.mode == "L"
