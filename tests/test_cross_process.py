import os

from PIL import Image

from anshitsu.process.cross_process import cross_process
from anshitsu.process.processor import Processor


def test_cross_process_returns_rgb_image():
    image = Image.new("RGB", (2, 2), (120, 130, 140))
    processed = cross_process(image, seed=1)

    assert processed.mode == "RGB"


def test_cross_process_changes_color():
    image = Image.new("RGB", (2, 2), (120, 130, 140))
    processed = cross_process(image, seed=1)

    assert processed.getpixel((0, 0)) != image.getpixel((0, 0))


def test_cross_process_seed_is_reproducible():
    image = Image.new("RGB", (2, 2), (120, 130, 140))

    first = cross_process(image, seed=7)
    second = cross_process(image, seed=7)

    assert first.tobytes() == second.tobytes()


def test_cross_process_seed_changes_result():
    image = Image.new("RGB", (2, 2), (120, 130, 140))

    first = cross_process(image, seed=7)
    second = cross_process(image, seed=8)

    assert first.tobytes() != second.tobytes()


def test_cross_process_by_rgb(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "dog.jpg"),
    )
    image = Processor(image=image, crossprocess=True).process()
    assert image.mode == "RGB"


def test_cross_process_by_grayscale(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "tokyo_station.jpg"),
    )
    image = Processor(image=image, crossprocess=True).process()
    assert image.mode == "RGB"


def test_cross_process_by_rgba(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "nullpo.png"),
    )
    image = Processor(image=image, crossprocess=True).process()
    assert image.mode == "RGB"


def test_cross_process_by_grayscale_with_alpha(setup):
    image = Image.open(
        os.path.join(".", "tests", "pic", "test.png"),
    )
    image = Processor(image=image, crossprocess=True).process()
    assert image.mode == "RGB"
