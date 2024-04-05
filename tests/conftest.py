import os.path
import os
import shutil
import subprocess

import pytest


@pytest.fixture()
def setup():
    shutil.copytree("./tests/pic", "./tests/pic_backup")
    yield
    abort()


def abort():
    shutil.rmtree("./tests/pic")
    shutil.copytree("./tests/pic_backup", "./tests/pic")
    shutil.rmtree("./tests/pic_backup")
