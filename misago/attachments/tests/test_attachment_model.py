from pathlib import Path

import pytest
from ..models import Attachment


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
    assert file_attachment.filetype.id == "txt"
    assert image_attachment.filetype.id == "png"


def test_attachment_delete_deletes_uploaded_file(file_attachment):
    upload_path = Path(file_attachment.upload.path)
    assert upload_path.exists()

    file_attachment.delete()

    assert not upload_path.exists()


def test_attachment_delete_deletes_thumbnail_file(image_thumbnail_attachment):
    upload_path = Path(image_thumbnail_attachment.upload.path)
    assert upload_path.exists()

    thumbnail_path = Path(image_thumbnail_attachment.thumbnail.path)
    assert thumbnail_path.exists()

    image_thumbnail_attachment.delete()

    assert not upload_path.exists()
    assert not thumbnail_path.exists()


def test_attachment_width_returns_width_from_dimensions():
    attachment = Attachment(dimensions="20x40")
    assert attachment.dimensions == "20x40"
    assert attachment.width == 20


def test_attachment_width_returns_none_if_dimensions_are_none():
    attachment = Attachment()
    assert attachment.dimensions is None
    assert attachment.width is None


def test_attachment_height_returns_height_from_dimensions():
    attachment = Attachment(dimensions="20x40")
    assert attachment.dimensions == "20x40"
    assert attachment.height == 40


def test_attachment_height_returns_none_if_dimensions_are_none():
    attachment = Attachment()
    assert attachment.dimensions is None
    assert attachment.height is None


def test_attachment_ratio_returns_ratio_from_dimensions():
    attachment = Attachment(dimensions="150x40")
    assert attachment.dimensions == "150x40"
    assert attachment.ratio == "26.67"


def test_attachment_height_returns_none_if_dimensions_are_none():
    attachment = Attachment()
    assert attachment.dimensions is None
    assert attachment.ratio is None
