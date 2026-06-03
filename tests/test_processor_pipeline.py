from PIL import Image

from anshitsu.process import processor
from anshitsu.process.processor import Processor


def test_processor_pipeline_order(monkeypatch):
    calls = []

    def stage(name):
        def apply(image, *args):
            calls.append(name)
            return image

        return apply

    monkeypatch.setattr(processor, "invert", stage("invert"))
    monkeypatch.setattr(processor, "color_auto_adjust", stage("color_auto_adjust"))
    monkeypatch.setattr(processor, "color_stretch", stage("color_stretch"))
    monkeypatch.setattr(processor, "rochester", stage("rochester"))
    monkeypatch.setattr(processor, "ashigara", stage("ashigara"))
    monkeypatch.setattr(processor, "cross_process", stage("cross_process"))
    monkeypatch.setattr(processor, "apocalypse", stage("apocalypse"))
    monkeypatch.setattr(processor, "ultramarine", stage("ultramarine"))
    monkeypatch.setattr(processor, "color", stage("color"))
    monkeypatch.setattr(processor, "brightness", stage("brightness"))
    monkeypatch.setattr(processor, "sharpness", stage("sharpness"))
    monkeypatch.setattr(processor, "posterize", stage("posterize"))

    def apply_grayscale(image):
        calls.append("grayscale")
        return Image.new("L", image.size)

    monkeypatch.setattr(processor, "grayscale", apply_grayscale)
    monkeypatch.setattr(processor, "orthochromatic", stage("orthochromatic"))
    monkeypatch.setattr(processor, "roppongi", stage("roppongi"))
    monkeypatch.setattr(processor, "classic", stage("classic"))
    monkeypatch.setattr(processor, "contrast", stage("contrast"))
    monkeypatch.setattr(processor, "line_drawing", stage("line_drawing"))
    monkeypatch.setattr(processor, "noise", stage("noise"))
    monkeypatch.setattr(processor, "vignette", stage("vignette"))
    monkeypatch.setattr(processor, "sepia", stage("sepia"))
    monkeypatch.setattr(processor, "cyanotype", stage("cyanotype"))
    monkeypatch.setattr(processor, "output_rgb", stage("output_rgb"))

    Processor(
        image=Image.new("RGB", (1, 1)),
        colorautoadjust=True,
        colorstretch=True,
        grayscale=True,
        orthochromatic=True,
        roppongi=True,
        classic=True,
        line_drawing=True,
        invert=True,
        outputrgb=True,
        noise=1.0,
        color=1.0,
        brightness=1.0,
        sharpness=1.0,
        contrast=1.0,
        sepia=True,
        cyanotype=True,
        rochester=True,
        ashigara=True,
        crossprocess=True,
        apocalypse=True,
        ultramarine=True,
        posterize=4,
        vignette=0.5,
    ).process()

    assert calls == [
        "invert",
        "color_auto_adjust",
        "color_stretch",
        "rochester",
        "ashigara",
        "cross_process",
        "apocalypse",
        "ultramarine",
        "color",
        "brightness",
        "sharpness",
        "posterize",
        "grayscale",
        "orthochromatic",
        "roppongi",
        "classic",
        "contrast",
        "line_drawing",
        "noise",
        "vignette",
        "sepia",
        "cyanotype",
        "output_rgb",
    ]


def test_toning_without_monochrome_preset_uses_grayscale():
    image = Image.new("RGB", (1, 1), (120, 140, 160))

    processed = Processor(image=image, sepia=True).process()

    assert processed.mode == "RGB"
    assert processed.getpixel((0, 0)) != image.getpixel((0, 0))
