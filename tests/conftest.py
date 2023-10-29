import os.path
import os
import shutil

import pytest

@pytest.fixture()
def setup():
    shutil.copytree("./tests/pic", "./tests/pic_backup")
    yield
    os.rmdir("./tests/pic")
    shutil.copytree("./tests/pic_backup", ".tests/pic")
    os.rmdir("./tests/pic_backup")