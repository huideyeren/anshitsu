import os

from PIL import Image

from anshitsu.process.create_alpha_mask import create_alpha_mask
from anshitsu.process.put_alpha_mask import put_alpha_mask

def test_alpha_mask_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    alpha = create_alpha_mask(image)
    assert alpha.mode == "L"


def test_alpha_mask_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    alpha = create_alpha_mask(image)
    assert alpha.mode == "L"

def test_alpha_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    alpha = create_alpha_mask(image)
    assert alpha is None

def test_alpha_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    alpha = create_alpha_mask(image)
    assert alpha is None

def test_alpha_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    alpha = create_alpha_mask(image)
    image.putalpha(alpha)
    assert image.mode == "RGBA"


def test_alpha_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    alpha = create_alpha_mask(image)
    image.putalpha(alpha)
    assert image.mode == "LA"
