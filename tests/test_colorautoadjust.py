import os

from anshitsu import retouch
from PIL import Image


def test_colorautoadjust_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    rt = retouch.Retouch(image=image, colorautoadjust=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_colorautoadjust_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    rt = retouch.Retouch(image=image, colorautoadjust=True)
    gray = rt.process()
    assert gray.mode == "L"


def test_colorautoadjust_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    rt = retouch.Retouch(image=image, colorautoadjust=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_colorautoadjust_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    rt = retouch.Retouch(image=image, colorautoadjust=True)
    gray = rt.process()
    assert gray.mode == "L"
