import os.path

import fire
import pytest
from anshitsu.process import process
from anshitsu.__version__ import version


def test_main_for_dir(capsys, setup):
    fire.Fire(process, ["./tests/pic", "--tosaka=2.4", "--outputrgb"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The process was completed successfully." in result


def test_main_for_image_file(capsys, setup):
    fire.Fire(process, ["./tests/pic/dog.jpg"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The process was completed successfully." in result


def test_main_for_invalid_directory(capfd, setup):
    with pytest.raises(SystemExit):
        fire.Fire(process, ["./src/anshitsu/"])
    captured = capfd.readouterr()
    error = captured.err

    assert "There are no JPEG or PNG files in this directory." in error


def test_main_for_invalid_file(capfd, setup):
    with pytest.raises(SystemExit):
        fire.Fire(process, ["./README.md"])
    captured = capfd.readouterr()
    error = captured.err

    assert "cannot identify image file" in error


def test_main_for_string_not_path(capfd, setup):
    with pytest.raises(SystemExit):
        fire.Fire(process, ["pic"])
    captured = capfd.readouterr()
    error = captured.err

    assert "A non-path string was passed." in error


def test_main_for_creating_directory_by_default(capfd, setup):
    fire.Fire(process, ["./tests/pic/dog.jpg"])
    captured = capfd.readouterr()
    error = captured.err

    assert os.path.exists("./tests/pic/anshitsu_out")


def test_main_for_creating_directory_by_overwrite_mode(capfd, setup):
    fire.Fire(process, ["./tests/pic/dog.jpg", "--overwrite", "--tosaka=2.4"])
    captured = capfd.readouterr()
    error = captured.err

    assert os.path.exists("./tests/pic/anshitsu_orig")


def test_main_for_saving_original_files_by_overwrite_mode(capfd, setup):
    fire.Fire(process, ["./tests/pic/dog.jpg",  "--overwrite", "--tosaka=2.4"])
    captured = capfd.readouterr()
    error = captured.err

    assert os.path.exists("./tests/pic/anshitsu_orig/dog.jpg")


def test_main_for_exist_converted_files_by_overwrite_mode(capfd, setup):
    fire.Fire(process, ["./tests/pic/dog.jpg",  "--overwrite", "--tosaka=2.4"])
    captured = capfd.readouterr()
    error = captured.err

    assert os.path.exists("./tests/pic/dog.png")


def test_main_for_show_version(capfd, setup):
    fire.Fire(process, ["--version"])
    captured = capfd.readouterr()
    result = captured.out

    assert "Anshitsu version {0}".format(version) in result


def test_main_for_no_path(capfd, setup):
    fire.Fire(process, [])
    captured = capfd.readouterr()
    error = captured.err

    assert "No path specified!" in error
