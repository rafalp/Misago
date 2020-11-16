import os

import pytest
from django.core.files.uploadedfile import UploadedFile
from django.urls import reverse

from ....test import assert_has_error_message

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def png_file():
    return os.path.join(TESTS_DIR, "images", "test.png")


@pytest.fixture
def svg_file():
    return os.path.join(TESTS_DIR, "images", "test.svg")


@pytest.fixture
def hashable_file():
    return os.path.join(TESTS_DIR, "css", "test.css")


@pytest.fixture
def hashed_file():
    return os.path.join(TESTS_DIR, "css", "test.4846cb3b.css")


@pytest.fixture
def upload(admin_client):
    def post_upload(theme, asset_files=None):
        url = reverse("misago:admin:themes:upload-media", kwargs={"pk": theme.pk})
        if asset_files is not None:
            data = asset_files if isinstance(asset_files, list) else [asset_files]
        else:
            data = ""
        return admin_client.post(url, {"assets": data})

    return post_upload


def test_font_file_can_be_uploaded(upload, theme):
    font_file = os.path.join(TESTS_DIR, "font", "Lato.ttf")
    with open(font_file, "rb") as fp:
        upload(theme, fp)
        assert theme.media.exists()


def test_text_file_can_be_uploaded(upload, theme):
    text_file = os.path.join(TESTS_DIR, "font", "OFL.txt")
    with open(text_file) as fp:
        upload(theme, fp)
        assert theme.media.exists()


def test_svg_file_can_be_uploaded(upload, theme):
    svg_file = os.path.join(TESTS_DIR, "images", "test.svg")
    with open(svg_file) as fp:
        upload(theme, fp)
        assert theme.media.exists()


def test_png_file_can_be_uploaded(upload, theme, png_file):
    with open(png_file, "rb") as fp:
        upload(theme, fp)
        assert theme.media.exists()


def test_media_file_name_is_set_as_asset_name(upload, theme, svg_file):
    with open(svg_file) as fp:
        upload(theme, fp)

    media = theme.media.last()
    expected_filename = str(svg_file).split("/")[-1]
    assert media.name == expected_filename


def test_media_file_is_uploaded_to_theme_directory(upload, theme, svg_file):
    with open(svg_file) as fp:
        upload(theme, fp)

    media = theme.media.last()
    assert theme.dirname in str(media.file)


def test_hash_is_added_to_uploaded_media_file_name(
    upload, theme, hashable_file, hashed_file
):
    with open(hashable_file) as fp:
        upload(theme, fp)

    media = theme.media.last()
    filename = str(media.file.path).split("/")[-1]
    expected_filename = str(hashed_file).split("/")[-1]
    assert filename == expected_filename


def test_hash_is_set_on_media_asset(upload, theme, hashed_file):
    with open(hashed_file) as fp:
        upload(theme, fp)

    media = theme.media.last()
    assert media.hash


def test_media_file_name_is_preserved_if_it_already_contains_correct_hash(
    upload, theme, hashed_file
):
    with open(hashed_file) as fp:
        upload(theme, fp)

    media = theme.media.last()
    filename = str(media.file.path).split("/")[-1]
    expected_filename = str(hashed_file).split("/")[-1]
    assert filename == expected_filename


def test_new_hash_is_added_to_media_file_name_if_it_contains_incorrect_hash(
    upload, theme
):
    incorrectly_hashed_file = os.path.join(TESTS_DIR, "css", "test.0046cb3b.css")
    with open(incorrectly_hashed_file) as fp:
        upload(theme, fp)

    media = theme.media.last()
    filename = str(media.file.path).split("/")[-1]
    assert media.hash in filename


def test_newly_uploaded_media_file_replaces_old_one_if_file_names_are_same(
    upload, theme, hashable_file
):
    with open(hashable_file) as fp:
        upload(theme, fp)
    original_media = theme.media.get()

    with open(os.path.join(TESTS_DIR, "css", "test-changed.css")) as fp:
        size = len(fp.read())
        fp.seek(0)
        upload(
            theme, UploadedFile(fp, name="test.css", content_type="text/css", size=size)
        )
    updated_media = theme.media.last()

    assert updated_media.name == original_media.name
    assert updated_media.hash != original_media.hash
    assert theme.media.count() == 1


def test_image_dimensions_are_set_for_uploaded_image_file(upload, theme, png_file):
    with open(png_file, "rb") as fp:
        upload(theme, fp)

    media = theme.media.last()
    assert media.width
    assert media.height


def test_thumbnail_is_generated_in_theme_directory_for_uploaded_image_file(
    upload, theme, png_file
):
    with open(png_file, "rb") as fp:
        upload(theme, fp)

    media = theme.media.last()
    assert theme.dirname in str(media.thumbnail)


def test_uploading_media_triggers_css_build(
    upload, theme, png_file, mock_build_theme_css
):
    with open(png_file, "rb") as fp:
        upload(theme, fp)

    mock_build_theme_css.assert_called_once_with(theme.pk)


def test_error_message_is_set_if_no_media_was_uploaded(upload, theme):
    response = upload(theme)
    assert_has_error_message(response)


def test_error_message_is_set_if_user_attempts_to_upload_file_to_default_theme(
    upload, default_theme
):
    response = upload(default_theme)
    assert_has_error_message(response)


def test_error_message_is_set_if_user_attempts_to_upload_file_to_nonexisting_theme(
    upload, nonexisting_theme
):
    response = upload(nonexisting_theme)
    assert_has_error_message(response)
