from pathlib import Path

import pytest
from ..models import Attachment


def test_attachment_get_new_secret_returns_secret_str():
    assert Attachment.get_new_secret()


@pytest.fixture
def file_attachment(user, text_file, attachment_factory):
    return attachment_factory(text_file, uploader=user)


@pytest.fixture
def image_attachment(user, image_small, attachment_factory):
    return attachment_factory(image_small, uploader=user)


@pytest.fixture
def image_thumbnail_attachment(user, image_large, image_small, attachment_factory):
    return attachment_factory(image_large, uploader=user, thumbnail_path=image_small)


def test_attachment_filetype_property_returns_filetype_instance(
    file_attachment, image_attachment
):
    assert file_attachment.filetype.name == "Text"
    assert image_attachment.filetype.name == "PNG"


def test_attachment_is_image_property_returns_true_for_file_attachment(
    file_attachment,
):
    assert file_attachment.is_file


def test_attachment_is_file_property_returns_false_for_image_attachment(
    image_attachment,
):
    assert not image_attachment.is_file


def test_attachment_is_image_property_returns_true_for_image_attachment(
    image_attachment,
):
    assert image_attachment.is_image


def test_attachment_is_image_property_returns_false_for_file_attachment(
    file_attachment,
):
    assert not file_attachment.is_image


def test_attachment_delete_deletes_file(file_attachment):
    file_path = Path(file_attachment.file.path)
    assert file_path.exists()

    file_attachment.delete()

    assert not file_path.exists()


def test_attachment_delete_deletes_image(image_attachment):
    image_path = Path(image_attachment.image.path)
    assert image_path.exists()

    image_attachment.delete()

    assert not image_path.exists()


def test_attachment_delete_deletes_image_thumbnail(image_thumbnail_attachment):
    image_path = Path(image_thumbnail_attachment.image.path)
    assert image_path.exists()

    thumbnail_path = Path(image_thumbnail_attachment.thumbnail.path)
    assert thumbnail_path.exists()

    image_thumbnail_attachment.delete()

    assert not image_path.exists()
    assert not thumbnail_path.exists()


def test_attachment_url_property_returns_file_url(file_attachment):
    assert file_attachment.url == file_attachment.file.url


def test_attachment_url_property_returns_image_url(image_attachment):
    assert image_attachment.url == image_attachment.image.url


def test_attachment_thumbnail_url_returns_none_if_thumbnail_is_not_set(
    image_attachment,
):
    assert image_attachment.thumbnail_url is None


def test_attachment_thumbnail_url_returns_thumbnail_url(image_thumbnail_attachment):
    attachment = image_thumbnail_attachment
    assert attachment.thumbnail_url == attachment.thumbnail.url
