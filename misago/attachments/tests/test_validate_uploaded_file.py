import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from ..validators import validate_uploaded_file


def test_validate_uploaded_file_passes_valid_file():
    file = SimpleUploadedFile("test.txt", "hello world".encode("utf-8"), "text/plain")
    validate_uploaded_file(file, max_size=1024)


def test_validate_uploaded_file_fails_file_with_invalid_mime_type():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.txt", "hello world".encode("utf-8"), "text/invalid"
        )
        validate_uploaded_file(file, max_size=1024)

    assert exc_info.value.message == "%(name)s: uploaded file type is not allowed."
    assert exc_info.value.code == "attachment_type"
    assert exc_info.value.params == {"name": "test.txt"}


def test_validate_uploaded_file_fails_file_with_invalid_extension_type():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.text", "hello world".encode("utf-8"), "text/plain"
        )
        validate_uploaded_file(file, max_size=1024)

    assert exc_info.value.message == "%(name)s: uploaded file type is not allowed."
    assert exc_info.value.code == "attachment_type"
    assert exc_info.value.params == {"name": "test.text"}


def test_validate_uploaded_file_fails_file_with_too_large_size():
    with pytest.raises(ValidationError) as exc_info:
        file = SimpleUploadedFile(
            "test.txt", "hello world".encode("utf-8"), "text/plain"
        )
        validate_uploaded_file(file, max_size=4)

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
    validate_uploaded_file(file, max_size=0)


def test_validate_uploaded_file_returns_file_type_for_valid_file():
    file = SimpleUploadedFile("test.txt", "hello world".encode("utf-8"), "text/plain")
    filetype = validate_uploaded_file(file, max_size=1024)
    assert filetype.name == "Text"
