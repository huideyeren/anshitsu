import os

from PIL import Image

from anshitsu.process.processor import Processor
from anshitsu.process.roppongi import _orthopanchromatic_grayscale, roppongi


def test_roppongi_returns_monochrome_image():
    image = Image.new("RGB", (8, 8), (128, 128, 128))
    processed = roppongi(image)

    assert processed.mode == "L"


def test_roppongi_compresses_highlights():
    image = Image.new("RGB", (8, 8), (245, 245, 245))
    processed = roppongi(image)

    assert max(processed.getdata()) < 255


def test_roppongi_response_is_mildly_orthopanchromatic():
    red = Image.new("RGB", (1, 1), (255, 0, 0))
    blue = Image.new("RGB", (1, 1), (0, 0, 255))

    red_gray = _orthopanchromatic_grayscale(red)
    blue_gray = _orthopanchromatic_grayscale(blue)

    assert red_gray.getpixel((0, 0)) < blue_gray.getpixel((0, 0))
    assert red_gray.getpixel((0, 0)) > 100


def test_roppongi_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, roppongi=True).process()
    assert image.mode == "L"


def test_roppongi_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, roppongi=True).process()
    assert image.mode == "L"


def test_roppongi_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, roppongi=True).process()
    assert image.mode == "L"


def test_roppongi_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, roppongi=True).process()
    assert image.mode == "L"
