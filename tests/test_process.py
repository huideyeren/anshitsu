import fire
import pytest
from anshitsu.process import process


def test_main_for_dir(capsys):
    fire.Fire(process, ["./tests/pic"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The process was completed successfully." in result


def test_main_for_file(capsys):
    fire.Fire(process, ["./tests/pic/dog.jpg"])
    captured = capsys.readouterr()
    result = captured.out
    assert "The process was completed successfully." in result


def test_main_error(capfd):
    with pytest.raises(SystemExit):
        fire.Fire(process, ["pic"])
    captured = capfd.readouterr()
    error = captured.err

    assert "A non-path string was passed." in error
