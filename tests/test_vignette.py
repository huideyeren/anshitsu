import os

from PIL import Image

from anshitsu.process.processor import Processor
from anshitsu.process.vignette import vignette


def test_vignette_darkens_rgb_edges():
    image = Image.new("RGB", (11, 11), (128, 128, 128))
    image = vignette(image, 1.0)

    center = image.getpixel((5, 5))[0]
    corner = image.getpixel((0, 0))[0]

    assert corner < center


def test_vignette_darkens_grayscale_edges():
    image = Image.new("L", (11, 11), 128)
    image = vignette(image, 1.0)

    center = image.getpixel((5, 5))
    corner = image.getpixel((0, 0))

    assert corner < center


def test_vignette_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, vignette=0.8).process()
    assert image.mode == "RGB"


def test_vignette_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, vignette=0.8).process()
    assert image.mode == "L"


def test_vignette_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, vignette=0.8).process()
    assert image.mode == "RGB"


def test_vignette_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, vignette=0.8).process()
    assert image.mode == "L"
