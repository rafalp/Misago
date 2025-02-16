from unittest.mock import Mock

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from ...conf.test import override_dynamic_settings
from ..filetypes import filetypes
from ..upload import store_uploaded_file


def test_store_uploaded_file_stores_text_file(
    user, dynamic_settings, text_file, teardown_attachments
):
    with open(text_file, "rb") as fp:
        upload = SimpleUploadedFile("test.txt", fp.read(), "text/plain")

    request = Mock(user=user, settings=dynamic_settings)
    filetype = filetypes.match_filetype(upload.name)

    attachment = store_uploaded_file(request, upload, filetype)

    assert attachment.id
    assert attachment.uploader == user
    assert attachment.uploader_name == user.username
    assert attachment.uploader_slug == user.slug
    assert attachment.uploaded_at
    assert attachment.name == upload.name
    assert attachment.slug == "test-txt"
    assert attachment.filetype_id == filetype.id
    assert not attachment.dimensions

    assert attachment.upload
    assert attachment.upload.url
    assert attachment.size == upload.size

    assert not attachment.thumbnail
    assert not attachment.thumbnail_size


def test_store_uploaded_file_stores_image_file(
    user, dynamic_settings, image_small, teardown_attachments
):
    with open(image_small, "rb") as fp:
        upload = SimpleUploadedFile("image.png", fp.read(), "image/png")

    request = Mock(user=user, settings=dynamic_settings)
    filetype = filetypes.match_filetype(upload.name)

    attachment = store_uploaded_file(request, upload, filetype)

    assert attachment.id
    assert attachment.uploader == user
    assert attachment.uploader_name == user.username
    assert attachment.uploader_slug == user.slug
    assert attachment.uploaded_at
    assert attachment.name == upload.name
    assert attachment.slug == "image-png"
    assert attachment.filetype_id == filetype.id
    assert attachment.dimensions == "50x50"

    assert attachment.upload
    assert attachment.upload.url
    assert attachment.size == upload.size

    assert not attachment.thumbnail
    assert not attachment.thumbnail_size


@override_dynamic_settings(
    attachment_thumbnail_width=400,
    attachment_thumbnail_height=300,
)
def test_store_uploaded_file_stores_image_file_with_thumbnail(
    user, dynamic_settings, image_large, teardown_attachments
):
    with open(image_large, "rb") as fp:
        upload = SimpleUploadedFile("image.png", fp.read(), "image/png")

    request = Mock(user=user, settings=dynamic_settings)
    filetype = filetypes.match_filetype(upload.name)

    attachment = store_uploaded_file(request, upload, filetype)

    assert attachment.id
    assert attachment.uploader == user
    assert attachment.uploader_name == user.username
    assert attachment.uploader_slug == user.slug
    assert attachment.uploaded_at
    assert attachment.name == upload.name
    assert attachment.slug == "image-png"
    assert attachment.filetype_id == filetype.id

    assert attachment.upload
    assert attachment.upload.url
    assert attachment.dimensions == "800x800"
    assert attachment.size == upload.size

    assert attachment.thumbnail
    assert attachment.thumbnail.url
    assert attachment.thumbnail_dimensions == "300x300"
    assert attachment.thumbnail_size


@override_dynamic_settings(
    attachment_image_max_width=400,
    attachment_image_max_height=300,
)
def test_store_uploaded_file_stores_image_file_scaled_down(
    user, dynamic_settings, image_large, teardown_attachments
):
    with open(image_large, "rb") as fp:
        upload = SimpleUploadedFile("image.png", fp.read(), "image/png")

    request = Mock(user=user, settings=dynamic_settings)
    filetype = filetypes.match_filetype(upload.name)

    attachment = store_uploaded_file(request, upload, filetype)

    assert attachment.id
    assert attachment.uploader == user
    assert attachment.uploader_name == user.username
    assert attachment.uploader_slug == user.slug
    assert attachment.uploaded_at
    assert attachment.name == upload.name
    assert attachment.slug == "image-png"
    assert attachment.filetype_id == filetype.id
    assert attachment.dimensions == "300x300"

    assert attachment.upload
    assert attachment.upload.url
    assert attachment.size == upload.size

    assert not attachment.thumbnail
    assert not attachment.thumbnail_size


def test_store_uploaded_file_cleans_filename(
    user, dynamic_settings, text_file, teardown_attachments
):
    with open(text_file, "rb") as fp:
        upload = SimpleUploadedFile("test (v2!).txt", fp.read(), "text/plain")

    request = Mock(user=user, settings=dynamic_settings)
    filetype = filetypes.match_filetype(upload.name)

    attachment = store_uploaded_file(request, upload, filetype)

    assert attachment.id
    assert attachment.uploader == user
    assert attachment.uploader_name == user.username
    assert attachment.uploader_slug == user.slug
    assert attachment.uploaded_at
    assert attachment.name == "test (v2!).txt"
    assert attachment.slug == "test-v2-txt"
    assert attachment.filetype_id == filetype.id
    assert not attachment.dimensions

    assert attachment.upload
    assert attachment.upload.url
    assert attachment.size == upload.size

    assert not attachment.thumbnail
    assert not attachment.thumbnail_size


def test_store_uploaded_file_stores_file_with_multiple_dots_in_name(
    user, dynamic_settings, text_file, teardown_attachments
):
    with open(text_file, "rb") as fp:
        upload = SimpleUploadedFile("test.final.txt", fp.read(), "text/plain")

    request = Mock(user=user, settings=dynamic_settings)
    filetype = filetypes.match_filetype(upload.name)

    attachment = store_uploaded_file(request, upload, filetype)

    assert attachment.id
    assert attachment.name == upload.name
    assert attachment.slug == "test-final-txt"
    assert attachment.filetype_id == filetype.id


def test_store_uploaded_file_raises_validation_error_for_invalid_image(
    user, dynamic_settings, image_invalid, teardown_attachments
):
    with open(image_invalid, "rb") as fp:
        upload = SimpleUploadedFile("image.png", fp.read(), "image/png")

    request = Mock(user=user, settings=dynamic_settings)
    filetype = filetypes.match_filetype(upload.name)

    with pytest.raises(ValidationError) as exc_info:
        store_uploaded_file(request, upload, filetype)

    assert exc_info.value.message == "Image file is not valid."
    assert exc_info.value.code == "unidentified_image"
