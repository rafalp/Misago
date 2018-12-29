import os

import pytest
from django.urls import reverse

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def css_file():
    return os.path.join(TESTS_DIR, "css", "test.css")


@pytest.fixture
def other_file():
    return os.path.join(TESTS_DIR, "images", "test.png")


@pytest.fixture
def hashed_css_file():
    return os.path.join(TESTS_DIR, "css", "test.4846cb3b.css")


@pytest.fixture
def incorrectly_hashed_css_file():
    return os.path.join(TESTS_DIR, "css", "test.0046cb3b.css")


@pytest.fixture
def upload(admin_client):
    def post_upload(theme, asset_files):
        url = reverse(
            "misago:admin:appearance:themes:upload-css", kwargs={"pk": theme.pk}
        )
        if asset_files:
            data = asset_files if isinstance(asset_files, list) else [asset_files]
        else:
            data = None
        return admin_client.post(url, {"assets": data})

    return post_upload


def test_css_file_can_be_uploaded(upload, theme, css_file):
    with open(css_file) as fp:
        upload(theme, fp)
        assert theme.css.exists()


def test_multiple_css_files_can_be_uploaded_at_once(
    upload, theme, css_file, hashed_css_file
):
    with open(css_file) as fp1:
        with open(hashed_css_file) as fp2:
            upload(theme, [fp1, fp2])
            assert theme.css.exists()
            assert theme.css.count() == 2


def test_uploaded_file_is_rejected_if_its_not_css_file(upload, theme, other_file):
    with open(other_file, "rb") as fp:
        upload(theme, fp)
        assert not theme.css.exists()


def test_if_some_of_uploaded_files_are_incorrect_only_correct_files_are_added_to_theme(
    upload, theme, css_file, other_file
):
    with open(css_file) as fp1:
        with open(other_file, "rb") as fp2:
            upload(theme, [fp1, fp2])
            assert theme.css.exists()
            assert theme.css.count() == 1

    css_asset = theme.css.last()
    expected_filename = str(css_file).split("/")[-1]
    assert css_asset.name == expected_filename


def test_css_file_is_uploaded_to_theme_directory(upload, theme, css_file):
    with open(css_file) as fp:
        upload(theme, fp)

    css_asset = theme.css.last()
    assert theme.dirname in str(css_asset.source_file)


def test_css_file_name_is_set_as_asset_name(upload, theme, css_file):
    with open(css_file) as fp:
        upload(theme, fp)

    css_asset = theme.css.last()
    expected_filename = str(css_file).split("/")[-1]
    assert css_asset.name == expected_filename


def test_hash_is_added_to_uploaded_file_name(upload, theme, css_file, hashed_css_file):
    with open(css_file) as fp:
        upload(theme, fp)

    css_asset = theme.css.last()
    filename = str(css_asset.source_file.path).split("/")[-1]
    expected_filename = str(hashed_css_file).split("/")[-1]
    assert filename == expected_filename


def test_hash_is_set_on_asset(upload, theme, css_file, hashed_css_file):
    with open(css_file) as fp:
        upload(theme, fp)

    css_asset = theme.css.last()
    assert css_asset.source_hash


def test_css_file_name_is_preserved_if_it_already_contains_correct_hash(
    upload, theme, hashed_css_file
):
    with open(hashed_css_file) as fp:
        upload(theme, fp)

    css_asset = theme.css.last()
    filename = str(css_asset.source_file.path).split("/")[-1]
    expected_filename = str(hashed_css_file).split("/")[-1]
    assert filename == expected_filename


def test_new_hash_is_added_to_css_file_name_if_it_contains_incorrect_hash(
    upload, theme, incorrectly_hashed_css_file
):
    with open(incorrectly_hashed_css_file) as fp:
        upload(theme, fp)

    css_asset = theme.css.last()
    filename = str(css_asset.source_file.path).split("/")[-1]
    assert css_asset.source_hash in filename
