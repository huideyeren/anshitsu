import os

from anshitsu import retouch
from PIL import Image


def test_output_rgb_by_rgb():
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    rt = retouch.Retouch(image=image, grayscale=True, outputrgb=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_output_rgb_by_grayscale():
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    rt = retouch.Retouch(image=image, grayscale=True, outputrgb=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_output_rgb_by_rgba():
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    rt = retouch.Retouch(image=image, grayscale=True, outputrgb=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_output_rgb_by_grayscale_with_alpha():
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    rt = retouch.Retouch(image=image, grayscale=True, outputrgb=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_output_rgb_by_rgb_using_tosaka_mode():
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    rt = retouch.Retouch(image=image, tosaka=2.4, outputrgb=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_output_rgb_by_grayscale_using_tosaka_mode():
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    rt = retouch.Retouch(image=image, tosaka=2.4, outputrgb=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_output_rgb_by_rgba_using_tosaka_mode():
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    rt = retouch.Retouch(image=image, tosaka=2.4, outputrgb=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_output_rgb_by_grayscale_with_alpha_using_tosaka_mode():
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    rt = retouch.Retouch(image=image, tosaka=2.4, outputrgb=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_output_rgb_by_rgb_with_none_grayscale_option():
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    rt = retouch.Retouch(image=image, outputrgb=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_output_rgb_by_grayscale_with_none_grayscale_option():
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    rt = retouch.Retouch(image=image, outputrgb=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_output_rgb_by_rgba_with_none_grayscale_option():
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    rt = retouch.Retouch(image=image, outputrgb=True)
    gray = rt.process()
    assert gray.mode == "RGB"


def test_output_rgb_by_grayscale_with_alpha_with_none_grayscale_option():
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    rt = retouch.Retouch(image=image, outputrgb=True)
    gray = rt.process()
    assert gray.mode == "RGB"
