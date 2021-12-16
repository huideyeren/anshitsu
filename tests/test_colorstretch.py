import os

from anshitsu import retouch
from PIL import Image


def test_colorstretch_by_rgb():
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    rt = retouch.Retouch(image=image, colorstretch=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_colorstretch_by_grayscale():
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    rt = retouch.Retouch(image=image, colorstretch=True)
    gray = rt.process()
    assert gray.mode == "L"


def test_colorstretch_by_rgba():
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    rt = retouch.Retouch(image=image, colorstretch=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_colorstretch_by_grayscale_with_alpha():
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    rt = retouch.Retouch(image=image, colorstretch=True)
    gray = rt.process()
    assert gray.mode == "L"
