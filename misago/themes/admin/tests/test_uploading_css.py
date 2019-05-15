import os

import pytest
from django.core.files.uploadedfile import UploadedFile
from django.urls import reverse

from ....test import assert_has_error_message

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
def upload(admin_client):
    def post_upload(theme, asset_files=None):
        url = reverse("misago:admin:themes:upload-css", kwargs={"pk": theme.pk})
        if asset_files is not None:
            data = asset_files if isinstance(asset_files, list) else [asset_files]
        else:
            data = ""
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


def test_css_files_uploaded_one_after_another_are_ordered(
    upload, theme, css_file, hashed_css_file
):
    with open(css_file) as fp:
        upload(theme, fp)
    first_css = theme.css.last()
    assert first_css.name == str(css_file).split("/")[-1]
    assert first_css.order == 0

    with open(hashed_css_file) as fp:
        upload(theme, fp)
    last_css = theme.css.last()
    assert last_css.name == str(hashed_css_file).split("/")[-1]
    assert last_css.order == 1


def test_multiple_css_files_uploaded_at_once_are_ordered(
    upload, theme, css_file, hashed_css_file
):
    with open(css_file) as fp1:
        with open(hashed_css_file) as fp2:
            upload(theme, [fp1, fp2])

    assert list(theme.css.values_list("name", flat=True)) == [
        str(css_file).split("/")[-1],
        str(hashed_css_file).split("/")[-1],
    ]
    assert list(theme.css.values_list("order", flat=True)) == [0, 1]


def test_uploaded_file_is_rejected_if_its_not_css_file(upload, theme, other_file):
    with open(other_file, "rb") as fp:
        upload(theme, fp)
        assert not theme.css.exists()


def test_error_message_is_set_if_uploaded_file_is_not_css(upload, theme, other_file):
    with open(other_file, "rb") as fp:
        response = upload(theme, fp)
        assert_has_error_message(response)


def test_if_some_of_uploaded_files_are_incorrect_only_css_files_are_added_to_theme(
    upload, theme, css_file, other_file
):
    with open(css_file) as fp1:
        with open(other_file, "rb") as fp2:
            upload(theme, [fp1, fp2])
            assert theme.css.exists()
            assert theme.css.count() == 1

    css = theme.css.last()
    expected_filename = str(css_file).split("/")[-1]
    assert css.name == expected_filename


def test_css_file_is_uploaded_to_theme_directory(upload, theme, css_file):
    with open(css_file) as fp:
        upload(theme, fp)

    css = theme.css.last()
    assert theme.dirname in str(css.source_file)


def test_css_file_name_is_set_as_asset_name(upload, theme, css_file):
    with open(css_file) as fp:
        upload(theme, fp)

    css = theme.css.last()
    expected_filename = str(css_file).split("/")[-1]
    assert css.name == expected_filename


def test_hash_is_added_to_uploaded_css_file_name(
    upload, theme, css_file, hashed_css_file
):
    with open(css_file) as fp:
        upload(theme, fp)

    css = theme.css.last()
    filename = str(css.source_file.path).split("/")[-1]
    expected_filename = str(hashed_css_file).split("/")[-1]
    assert filename == expected_filename


def test_hash_is_set_on_css_source_asset(upload, theme, css_file):
    with open(css_file) as fp:
        upload(theme, fp)

    css = theme.css.last()
    assert css.source_hash


def test_css_file_name_is_preserved_if_it_already_contains_correct_hash(
    upload, theme, hashed_css_file
):
    with open(hashed_css_file) as fp:
        upload(theme, fp)

    css = theme.css.last()
    filename = str(css.source_file.path).split("/")[-1]
    expected_filename = str(hashed_css_file).split("/")[-1]
    assert filename == expected_filename


def test_new_hash_is_added_to_css_file_name_if_it_contains_incorrect_hash(
    upload, theme
):
    incorrectly_hashed_css_file = os.path.join(TESTS_DIR, "css", "test.0046cb3b.css")
    with open(incorrectly_hashed_css_file) as fp:
        upload(theme, fp)

    css = theme.css.last()
    filename = str(css.source_file.path).split("/")[-1]
    assert css.source_hash in filename


def test_newly_uploaded_css_file_replaces_old_one_if_file_names_are_same(
    upload, theme, css_file
):
    with open(css_file) as fp:
        upload(theme, fp)
    original_css = theme.css.get()

    with open(os.path.join(TESTS_DIR, "css", "test-changed.css")) as fp:
        size = len(fp.read())
        fp.seek(0)
        upload(
            theme, UploadedFile(fp, name="test.css", content_type="text/css", size=size)
        )
    updated_css = theme.css.last()

    assert updated_css.name == original_css.name
    assert updated_css.source_hash != original_css.source_hash
    assert theme.css.count() == 1


def test_newly_uploaded_css_file_reuses_replaced_file_order_if_names_are_same(
    upload, theme, css_file, hashed_css_file
):
    with open(css_file) as fp:
        upload(theme, fp)
    original_css = theme.css.last()

    with open(hashed_css_file) as fp:
        upload(theme, fp)

    with open(os.path.join(TESTS_DIR, "css", "test-changed.css")) as fp:
        size = len(fp.read())
        fp.seek(0)
        upload(
            theme, UploadedFile(fp, name="test.css", content_type="text/css", size=size)
        )

    updated_css = theme.css.get(order=original_css.order)
    assert updated_css.name == original_css.name


def test_if_uploaded_css_file_contains_no_image_urls_rebuild_flag_is_not_set(
    upload, theme, css_file
):
    with open(css_file) as fp:
        upload(theme, fp)

    css = theme.css.last()
    assert not css.source_needs_building


def test_if_uploaded_css_file_contains_image_url_it_has_rebuild_flag_set(upload, theme):
    css_file = os.path.join(TESTS_DIR, "css", "test.needs-build.css")
    with open(css_file) as fp:
        upload(theme, fp)

    css = theme.css.last()
    assert css.source_needs_building


def test_uploading_css_file_triggers_css_build(
    upload, theme, css_file, mock_build_theme_css
):
    with open(css_file) as fp:
        upload(theme, fp)

    mock_build_theme_css.assert_called_once_with(theme.pk)


def test_error_message_is_set_if_no_css_file_was_uploaded(upload, theme):
    response = upload(theme)
    assert_has_error_message(response)


def test_error_message_is_set_if_user_attempts_to_upload_css_file_to_default_theme(
    upload, default_theme
):
    response = upload(default_theme)
    assert_has_error_message(response)


def test_error_message_is_set_if_user_attempts_to_upload_css_file_to_nonexisting_theme(
    upload, nonexisting_theme
):
    response = upload(nonexisting_theme)
    assert_has_error_message(response)
