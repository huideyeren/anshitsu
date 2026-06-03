import fire
import pytest

from anshitsu.__version__ import version
from anshitsu.cli import cli


def test_main_for_dir(capsys, setup):
    fire.Fire(cli, [str(setup), "--tosaka=2.4", "--outputrgb"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_image_file(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg")])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_vignette(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--vignette=0.8"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_rochester(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--rochester"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_ashigara(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--ashigara"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_crossprocess(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--crossprocess"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_apocalypse(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--apocalypse"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_orthochromatic(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--orthochromatic"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_roppongi(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--roppongi"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_classic(capsys, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--classic"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The cli was completed successfully." in result


def test_main_for_invalid_directory(capfd, setup):
    with pytest.raises(SystemExit):
        fire.Fire(cli, ["./src/anshitsu/"])
    captured = capfd.readouterr()
    error = captured.err

    assert "There are no JPEG or PNG files in this directory." in error


def test_main_for_invalid_file(capfd, setup):
    with pytest.raises(SystemExit):
        fire.Fire(cli, ["./README.md"])
    captured = capfd.readouterr()
    error = captured.err

    assert "cannot identify image file" in error


def test_main_for_string_not_path(capfd, setup):
    with pytest.raises(SystemExit):
        fire.Fire(cli, ["pic"])
    captured = capfd.readouterr()
    error = captured.err

    assert "A non-path string was passed." in error


def test_main_for_creating_directory_by_default(capfd, setup):
    fire.Fire(cli, [str(setup / "dog.jpg")])
    captured = capfd.readouterr()
    error = captured.err

    assert (setup / "anshitsu_out").exists()


def test_main_for_creating_directory_by_overwrite_mode(capfd, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--overwrite", "--tosaka=2.4"])
    captured = capfd.readouterr()
    error = captured.err

    assert (setup / "anshitsu_orig").exists()


def test_main_for_saving_original_files_by_overwrite_mode(capfd, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--overwrite", "--tosaka=2.4"])
    captured = capfd.readouterr()
    error = captured.err

    assert (setup / "anshitsu_orig/dog.jpg").exists()


def test_main_for_exist_converted_files_by_overwrite_mode(capfd, setup):
    fire.Fire(cli, [str(setup / "dog.jpg"), "--overwrite", "--tosaka=2.4"])
    captured = capfd.readouterr()
    error = captured.err

    assert (setup / "dog.png").exists()


def test_main_for_show_version(capfd, setup):
    fire.Fire(cli, ["--version"])
    captured = capfd.readouterr()
    result = captured.out

    assert "Anshitsu version {0}".format(version) in result


def test_main_for_no_path(capfd, setup):
    with pytest.raises(SystemExit):
        fire.Fire(cli, [])
    captured = capfd.readouterr()
    error = captured.err

    assert "No path specified!" in error
