import fire
import pytest
from anshitsu.process import process
from PIL import UnidentifiedImageError


def test_main_for_dir(capsys):
    fire.Fire(process, ["./tests/pic", "--tosaka=2.4", "--outputrgb"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The process was completed successfully." in result


def test_main_for_image_file(capsys):
    fire.Fire(process, ["./tests/pic/dog.jpg"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The process was completed successfully." in result


def test_main_for_invalid_directory(capfd):
    with pytest.raises(SystemExit):
        fire.Fire(process, ["./src/anshitsu/"])
    captured = capfd.readouterr()
    error = captured.err

    assert "There are no JPEG or PNG files in this directory." in error


def test_main_for_invalid_file(capfd):
    with pytest.raises(SystemExit):
        fire.Fire(process, ["./README.md"])
    captured = capfd.readouterr()
    error = captured.err

    assert "cannot identify image file" in error


def test_main_for_string_not_path(capfd):
    with pytest.raises(SystemExit):
        fire.Fire(process, ["pic"])
    captured = capfd.readouterr()
    error = captured.err

    assert "A non-path string was passed." in error
