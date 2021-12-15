import os

from anshitsu import retouch
from PIL import Image


def test_grayscale_by_rgb():
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    rt = retouch.Retouch(image=image, grayscale=True)
    gray = rt.process()
    assert gray.mode == "L"


def test_grayscale_by_grayscale():
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    rt = retouch.Retouch(image=image, grayscale=True)
    gray = rt.process()
    assert gray.mode == "L"


def test_grayscale_by_rgba():
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    rt = retouch.Retouch(image=image, grayscale=True)
    gray = rt.process()
    assert gray.mode == "L"
