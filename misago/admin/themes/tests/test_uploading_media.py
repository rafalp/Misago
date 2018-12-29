import os

import pytest
from django.urls import reverse

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def font_file():
    return os.path.join(TESTS_DIR, "font", "Lato.ttf")


@pytest.fixture
def text_file():
    return os.path.join(TESTS_DIR, "font", "OFL.txt")


@pytest.fixture
def png_file():
    return os.path.join(TESTS_DIR, "images", "test.png")


@pytest.fixture
def svg_file():
    return os.path.join(TESTS_DIR, "images", "test.svg")


@pytest.fixture
def upload(admin_client):
    def post_upload(theme, asset_files):
        url = reverse(
            "misago:admin:appearance:themes:upload-media", kwargs={"pk": theme.pk}
        )
        if asset_files:
            data = asset_files if isinstance(asset_files, list) else [asset_files]
        else:
            data = None
        return admin_client.post(url, {"assets": data})

    return post_upload


def test_font_file_can_be_uploaded(upload, theme, font_file):
    with open(font_file, "rb") as fp:
        upload(theme, fp)
        assert theme.media.exists()


def test_text_file_can_be_uploaded(upload, theme, text_file):
    with open(text_file) as fp:
        upload(theme, fp)
        assert theme.media.exists()


def test_png_file_can_be_uploaded(upload, theme, png_file):
    with open(png_file, "rb") as fp:
        upload(theme, fp)
        assert theme.media.exists()


def test_svg_file_can_be_uploaded(upload, theme, svg_file):
    with open(svg_file) as fp:
        upload(theme, fp)
        assert theme.media.exists()
