import os

import pytest
from starlette.datastructures import UploadFile

TEST_AVATAR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "avatar.png"
)


@pytest.fixture
def avatar_path():
    return TEST_AVATAR_PATH


@pytest.fixture
def uploaded_image(avatar_path):
    upload = UploadFile("avatar.png")
    with open(avatar_path, "rb") as fp:
        upload.file.write(fp.read())
    return upload
