import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from ..enums import AllowedAttachments, AttachmentStorage
from ..validators import validate_uploaded_file


def test_validate_uploaded_file_passes_valid_file():
    file = SimpleUploadedFile("test.txt", "hello world".encode("utf-8"), "text/plain")
    validate_uploaded_file(
        file, allowed_attachments=AllowedAttachments.ALL, max_size=1024
    )


def test_validate_uploaded_file_fails_file_with_invalid_mime_type():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.txt", "hello world".encode("utf-8"), "text/invalid"
        )
        validate_uploaded_file(
            file, allowed_attachments=AllowedAttachments.ALL, max_size=1024
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
            file,
            allowed_attachments=AllowedAttachments.ALL,
            max_size=1024,
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
            file,
            allowed_attachments=AllowedAttachments.MEDIA,
            max_size=1024,
        )

    assert exc_info.value.message == "%(name)s: uploaded file type is not allowed."
    assert exc_info.value.code == "attachment_type"
    assert exc_info.value.params == {"name": "test.txt"}


def test_validate_uploaded_file_passes_video_file_as_media():
    file = SimpleUploadedFile("test.mp4", "hello world".encode("utf-8"), "video/mp4")
    validate_uploaded_file(
        file,
        allowed_attachments=AllowedAttachments.MEDIA,
        max_size=1024,
    )


def test_validate_uploaded_file_passes_image_file_as_media():
    file = SimpleUploadedFile("test.png", "hello world".encode("utf-8"), "image/png")
    validate_uploaded_file(
        file,
        allowed_attachments=AllowedAttachments.MEDIA,
        max_size=1024,
    )


def test_validate_uploaded_file_fails_text_file_as_image():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.txt", "hello world".encode("utf-8"), "text/plain"
        )
        validate_uploaded_file(
            file,
            allowed_attachments=AllowedAttachments.IMAGES,
            max_size=1024,
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
            file,
            allowed_attachments=AllowedAttachments.IMAGES,
            max_size=1024,
        )

    assert exc_info.value.message == "%(name)s: uploaded file type is not allowed."
    assert exc_info.value.code == "attachment_type"
    assert exc_info.value.params == {"name": "test.mp4"}


def test_validate_uploaded_file_passes_image_file_as_image():
    file = SimpleUploadedFile("test.png", "hello world".encode("utf-8"), "image/png")
    validate_uploaded_file(
        file,
        allowed_attachments=AllowedAttachments.IMAGES,
        max_size=1024,
    )


def test_validate_uploaded_file_fails_file_with_too_large_size():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.txt", "hello world".encode("utf-8"), "text/plain"
        )
        validate_uploaded_file(
            file,
            allowed_attachments=AllowedAttachments.ALL,
            max_size=4,
        )

    assert exc_info.value.message == (
        "%(name)s: uploaded file cannot exceed %(limit_value)s in size "
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
    validate_uploaded_file(
        file,
        allowed_attachments=AllowedAttachments.ALL,
        max_size=0,
    )


def test_validate_uploaded_file_passes_file_with_storage_limit_disabled():
    file = SimpleUploadedFile("test.txt", "hello world".encode("utf-8"), "text/plain")
    validate_uploaded_file(
        file,
        allowed_attachments=AllowedAttachments.ALL,
        max_size=0,
        storage=None,
        storage_limit=0,
        storage_left=0,
    )


def test_validate_uploaded_file_passes_file_with_enough_storage():
    file = SimpleUploadedFile("test.txt", "hello world".encode("utf-8"), "text/plain")
    validate_uploaded_file(
        file,
        allowed_attachments=AllowedAttachments.ALL,
        max_size=0,
        storage=AttachmentStorage.USER_TOTAL,
        storage_limit=1024,
        storage_left=file.size,
    )


def test_validate_uploaded_file_fails_file_after_global_storage_runs_out():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.txt", "hello world".encode("utf-8"), "text/plain"
        )
        validate_uploaded_file(
            file,
            allowed_attachments=AllowedAttachments.ALL,
            max_size=0,
            storage=AttachmentStorage.GLOBAL,
            storage_limit=1024,
            storage_left=0,
        )

    assert (
        exc_info.value.message
        == "%(name)s: uploaded file exceeds the remaining attachments space (%(limit_value)s)."
    )
    assert exc_info.value.code == "attachments_global_storage_left"
    assert exc_info.value.params == {"name": "test.txt", "limit_value": "0\xa0bytes"}


def test_validate_uploaded_file_fails_file_after_user_storage_runs_out():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.txt", "hello world".encode("utf-8"), "text/plain"
        )
        validate_uploaded_file(
            file,
            allowed_attachments=AllowedAttachments.ALL,
            max_size=0,
            storage=AttachmentStorage.USER_TOTAL,
            storage_limit=1024,
            storage_left=0,
        )

    assert (
        exc_info.value.message
        == "%(name)s: uploaded file exceeds your remaining attachment space (%(limit_value)s)."
    )
    assert exc_info.value.code == "attachments_storage_left"
    assert exc_info.value.params == {"name": "test.txt", "limit_value": "0\xa0bytes"}


def test_validate_uploaded_file_fails_file_after_user_unused_storage_runs_out():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.txt", "hello world".encode("utf-8"), "text/plain"
        )
        validate_uploaded_file(
            file,
            allowed_attachments=AllowedAttachments.ALL,
            max_size=0,
            storage=AttachmentStorage.USER_UNUSED,
            storage_limit=1024,
            storage_left=0,
        )

    assert (
        exc_info.value.message
        == "%(name)s: uploaded file exceeds your remaining attachment space (%(limit_value)s)."
    )
    assert exc_info.value.code == "attachments_storage_left"
    assert exc_info.value.params == {"name": "test.txt", "limit_value": "0\xa0bytes"}


def test_validate_uploaded_file_returns_file_type_for_valid_file():
    file = SimpleUploadedFile("test.txt", "hello world".encode("utf-8"), "text/plain")
    filetype = validate_uploaded_file(
        file,
        allowed_attachments=AllowedAttachments.ALL,
        max_size=1024,
    )
    assert filetype.id == "txt"
