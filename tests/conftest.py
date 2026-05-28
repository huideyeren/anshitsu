import shutil
from pathlib import Path

import pytest


@pytest.fixture()
def setup(tmp_path):
    work_dir = tmp_path / "pic"
    shutil.copytree(Path("tests/pic"), work_dir)
    return work_dir
