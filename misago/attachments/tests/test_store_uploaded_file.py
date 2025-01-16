from unittest.mock import Mock

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from ...conf.test import override_dynamic_settings
from ..filetypes import filetypes
from ..store import store_uploaded_file


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
    assert attachment.secret
    assert attachment.filename == upload.name
    assert attachment.size == upload.size
    assert attachment.filetype_name == filetype.name
    assert not attachment.dimensions

    assert not attachment.thumbnail
    assert not attachment.image
    assert not attachment.video
    assert attachment.file
    assert attachment.file.url


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
    assert attachment.secret
    assert attachment.filename == upload.name
    assert attachment.size == upload.size
    assert attachment.filetype_name == filetype.name
    assert attachment.dimensions == "50x50"

    assert not attachment.thumbnail
    assert attachment.image
    assert attachment.image.url
    assert not attachment.video
    assert not attachment.file


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
    assert attachment.secret
    assert attachment.filename == upload.name
    assert attachment.size == upload.size
    assert attachment.filetype_name == filetype.name
    assert attachment.dimensions == "800x800"

    assert attachment.thumbnail
    assert attachment.thumbnail.url
    assert attachment.image
    assert attachment.image.url
    assert not attachment.video
    assert not attachment.file


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
    assert attachment.secret
    assert attachment.filename == upload.name
    assert attachment.size == upload.size
    assert attachment.filetype_name == filetype.name
    assert attachment.dimensions == "300x300"

    assert not attachment.thumbnail
    assert attachment.image
    assert attachment.image.url
    assert not attachment.video
    assert not attachment.file


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
    assert attachment.secret
    assert attachment.filename == "test-v2.txt"
    assert attachment.size == upload.size
    assert attachment.filetype_name == filetype.name
    assert not attachment.dimensions

    assert not attachment.thumbnail
    assert not attachment.image
    assert not attachment.video
    assert attachment.file
    assert attachment.file.url


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
