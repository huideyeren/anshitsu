import os

from anshitsu import retouch
from PIL import Image


def test_grayscale_by_rgb():
    img = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    rt = retouch.Retouch(img)
    gray = rt.process(grayscale=True)
    assert gray.mode == "L"


def test_grayscale_by_grayscale():
    img = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    rt = retouch.Retouch(img)
    gray = rt.process(grayscale=True)
    assert gray.mode == "L"


def test_grayscale_by_rgba():
    img = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    rt = retouch.Retouch(img)
    gray = rt.process(grayscale=True)
    assert gray.mode == "L"
