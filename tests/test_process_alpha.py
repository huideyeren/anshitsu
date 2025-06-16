import os

from PIL import Image

from anshitsu.process.processor import Processor

def test_process_alpha_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, keep_alpha=True).process()
    assert image.mode == "RGB"


def test_process_alpha_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, keep_alpha=True).process()
    assert image.mode == "L"


def test_process_alpha_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, keep_alpha=True).process()
    assert image.mode == "RGBA"


def test_process_alpha_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, keep_alpha=True).process()
    assert image.mode == "LA"