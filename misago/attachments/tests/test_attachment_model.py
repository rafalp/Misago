from pathlib import Path

import pytest
from ..models import Attachment


def test_attachment_filetype_property_returns_filetype_instance(
    text_attachment, image_attachment, video_attachment
):
    assert text_attachment.filetype.id == "txt"
    assert image_attachment.filetype.id == "png"
    assert video_attachment.filetype.id == "mp4"


def test_attachment_delete_deletes_uploaded_file(text_file, attachment_factory):
    attachment = attachment_factory(text_file)

    upload_path = Path(attachment.upload.path)
    assert upload_path.exists()

    attachment.delete()

    assert not upload_path.exists()

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()


def test_attachment_delete_deletes_thumbnail_file(
    image_large, image_small, attachment_factory
):
    attachment = attachment_factory(image_large, thumbnail_path=image_small)

    upload_path = Path(attachment.upload.path)
    assert upload_path.exists()

    thumbnail_path = Path(attachment.thumbnail.path)
    assert thumbnail_path.exists()

    attachment.delete()

    assert not upload_path.exists()
    assert not thumbnail_path.exists()

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()


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
    assert attachment.ratio is None


def test_attachment_ratio_returns_ratio_from_dimensions():
    attachment = Attachment(dimensions="150x40")
    assert attachment.dimensions == "150x40"
    assert attachment.ratio == "26.67"


def test_attachment_thumbnail_width_returns_width_from_thumbnail_dimensions():
    attachment = Attachment(thumbnail_dimensions="20x40")
    assert attachment.thumbnail_dimensions == "20x40"
    assert attachment.thumbnail_width == 20


def test_attachment_thumbnail_width_returns_none_if_thumbnail_dimensions_are_none():
    attachment = Attachment()
    assert attachment.thumbnail_dimensions is None
    assert attachment.thumbnail_width is None


def test_attachment_thumbnail_height_returns_height_from_thumbnail_dimensions():
    attachment = Attachment(thumbnail_dimensions="20x40")
    assert attachment.thumbnail_dimensions == "20x40"
    assert attachment.thumbnail_height == 40


def test_attachment_thumbnail_height_returns_none_if_thumbnail_dimensions_are_none():
    attachment = Attachment()
    assert attachment.thumbnail_dimensions is None
    assert attachment.thumbnail_height is None
