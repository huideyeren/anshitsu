import os

from PIL import Image

from anshitsu.process.apocalypse import apocalypse
from anshitsu.process.processor import Processor


def test_apocalypse_returns_rgb_image():
    image = Image.new("RGB", (2, 2), (120, 130, 140))
    processed = apocalypse(image, seed=1)

    assert processed.mode == "RGB"


def test_apocalypse_shifts_neutral_toward_red_orange():
    image = Image.new("RGB", (2, 2), (120, 120, 120))
    processed = apocalypse(image, seed=1)
    red, green, blue = processed.getpixel((0, 0))

    assert red > green > blue


def test_apocalypse_preserves_highlight_detail():
    image = Image.new("RGB", (2, 2), (245, 245, 245))
    processed = apocalypse(image, seed=1)

    assert max(processed.getpixel((0, 0))) < 255


def test_apocalypse_seed_is_reproducible():
    image = Image.new("RGB", (2, 2), (120, 130, 140))

    first = apocalypse(image, seed=7)
    second = apocalypse(image, seed=7)

    assert first.tobytes() == second.tobytes()


def test_apocalypse_seed_changes_red_shift_strength():
    image = Image.new("RGB", (2, 2), (120, 130, 140))

    first = apocalypse(image, seed=7)
    second = apocalypse(image, seed=8)

    assert first.tobytes() != second.tobytes()


def test_apocalypse_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, apocalypse=True).process()
    assert image.mode == "RGB"


def test_apocalypse_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, apocalypse=True).process()
    assert image.mode == "RGB"


def test_apocalypse_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, apocalypse=True).process()
    assert image.mode == "RGB"


def test_apocalypse_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, apocalypse=True).process()
    assert image.mode == "RGB"
