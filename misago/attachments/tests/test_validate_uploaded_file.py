import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from ..enums import AllowedAttachments
from ..validators import validate_uploaded_file


def test_validate_uploaded_file_passes_valid_file():
    file = SimpleUploadedFile("test.txt", "hello world".encode("utf-8"), "text/plain")
    validate_uploaded_file(
        file, max_size=1024, allowed_attachments=AllowedAttachments.ALL
    )


def test_validate_uploaded_file_fails_file_with_invalid_mime_type():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.txt", "hello world".encode("utf-8"), "text/invalid"
        )
        validate_uploaded_file(
            file, max_size=1024, allowed_attachments=AllowedAttachments.ALL
        )

    assert exc_info.value.message == "%(name)s: uploaded file type is not allowed."
    assert exc_info.value.code == "attachment_type"
    assert exc_info.value.params == {"name": "test.txt"}


def test_validate_uploaded_file_fails_file_with_invalid_extension_type():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.text", "hello world".encode("utf-8"), "text/plain"
        )
        validate_uploaded_file(
            file, max_size=1024, allowed_attachments=AllowedAttachments.ALL
        )

    assert exc_info.value.message == "%(name)s: uploaded file type is not allowed."
    assert exc_info.value.code == "attachment_type"
    assert exc_info.value.params == {"name": "test.text"}


def test_validate_uploaded_file_fails_text_file_as_media():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.txt", "hello world".encode("utf-8"), "text/plain"
        )
        validate_uploaded_file(
            file, max_size=1024, allowed_attachments=AllowedAttachments.MEDIA
        )

    assert exc_info.value.message == "%(name)s: uploaded file type is not allowed."
    assert exc_info.value.code == "attachment_type"
    assert exc_info.value.params == {"name": "test.txt"}


def test_validate_uploaded_file_passes_video_file_as_media():
    file = SimpleUploadedFile("test.mp4", "hello world".encode("utf-8"), "video/mp4")
    validate_uploaded_file(
        file, max_size=1024, allowed_attachments=AllowedAttachments.MEDIA
    )


def test_validate_uploaded_file_passes_image_file_as_media():
    file = SimpleUploadedFile("test.png", "hello world".encode("utf-8"), "image/png")
    validate_uploaded_file(
        file, max_size=1024, allowed_attachments=AllowedAttachments.MEDIA
    )


def test_validate_uploaded_file_fails_text_file_as_image():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.txt", "hello world".encode("utf-8"), "text/plain"
        )
        validate_uploaded_file(
            file, max_size=1024, allowed_attachments=AllowedAttachments.IMAGES
        )

    assert exc_info.value.message == "%(name)s: uploaded file type is not allowed."
    assert exc_info.value.code == "attachment_type"
    assert exc_info.value.params == {"name": "test.txt"}


def test_validate_uploaded_file_fails_video_file_as_image():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.mp4", "hello world".encode("utf-8"), "video/mp4"
        )
        validate_uploaded_file(
            file, max_size=1024, allowed_attachments=AllowedAttachments.IMAGES
        )

    assert exc_info.value.message == "%(name)s: uploaded file type is not allowed."
    assert exc_info.value.code == "attachment_type"
    assert exc_info.value.params == {"name": "test.mp4"}


def test_validate_uploaded_file_passes_image_file_as_image():
    file = SimpleUploadedFile("test.png", "hello world".encode("utf-8"), "image/png")
    validate_uploaded_file(
        file, max_size=1024, allowed_attachments=AllowedAttachments.IMAGES
    )


def test_validate_uploaded_file_fails_file_with_too_large_size():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.txt", "hello world".encode("utf-8"), "text/plain"
        )
        validate_uploaded_file(
            file, max_size=4, allowed_attachments=AllowedAttachments.ALL
        )

    assert exc_info.value.message == (
        "%(name)s: uploaded file cannot be larger than %(limit_value)s "
        "(it has %(show_value)s)."
    )
    assert exc_info.value.code == "attachment_size"
    assert exc_info.value.params == {
        "name": "test.txt",
        "limit_value": "4\xa0bytes",
        "show_value": "11\xa0bytes",
    }


def test_validate_uploaded_file_passes_file_with_size_limit_disabled():
    file = SimpleUploadedFile("test.txt", "hello world".encode("utf-8"), "text/plain")
    validate_uploaded_file(file, max_size=0, allowed_attachments=AllowedAttachments.ALL)


def test_validate_uploaded_file_returns_file_type_for_valid_file():
    file = SimpleUploadedFile("test.txt", "hello world".encode("utf-8"), "text/plain")
    filetype = validate_uploaded_file(
        file, max_size=1024, allowed_attachments=AllowedAttachments.ALL
    )
    assert filetype.name == "Text"
