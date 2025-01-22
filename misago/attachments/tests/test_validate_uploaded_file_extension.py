import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from ..enums import AttachmentTypeRestriction
from ..validators import (
    validate_uploaded_file_disallowed_extension,
    validate_uploaded_file_extension,
    validate_uploaded_file_required_extension,
)


def test_validate_uploaded_file_extension_does_nothing_if_extensions_list_is_empty():
    upload = SimpleUploadedFile("test.txt", b"test", content_type="text/plain")
    validate_uploaded_file_extension(upload, AttachmentTypeRestriction.REQUIRE, [])
    validate_uploaded_file_extension(upload, AttachmentTypeRestriction.DISALLOW, [])


def test_validate_uploaded_file_extension_passes_file_if_its_extension_is_on_required_list():
    upload = SimpleUploadedFile("test.txt", b"test", content_type="text/plain")
    validate_uploaded_file_extension(upload, AttachmentTypeRestriction.REQUIRE, ["txt"])


def test_validate_uploaded_file_extension_fails_file_if_its_extension_is_not_on_required_list():
    upload = SimpleUploadedFile("test.txt", b"test", content_type="text/plain")

    with pytest.raises(ValidationError):
        validate_uploaded_file_extension(
            upload, AttachmentTypeRestriction.REQUIRE, ["pdf"]
        )


def test_validate_uploaded_file_extension_passes_file_if_its_extension_is_not_on_disallowed_list():
    upload = SimpleUploadedFile("test.txt", b"test", content_type="text/plain")
    validate_uploaded_file_extension(
        upload, AttachmentTypeRestriction.DISALLOW, ["pdf"]
    )


def test_validate_uploaded_file_extension_fails_file_if_its_extension_is_on_disallowed_list():
    upload = SimpleUploadedFile("test.txt", b"test", content_type="text/plain")

    with pytest.raises(ValidationError):
        validate_uploaded_file_extension(
            upload, AttachmentTypeRestriction.DISALLOW, ["txt"]
        )


def test_validate_uploaded_file_required_extension_extension_does_nothing_if_extensions_list_is_empty():
    upload = SimpleUploadedFile("test.txt", b"test", content_type="text/plain")
    validate_uploaded_file_required_extension(upload, [])


def test_validate_uploaded_file_required_extension_extension_passes_file_if_its_extension_is_on_extensions_list():
    upload = SimpleUploadedFile("test.txt", b"test", content_type="text/plain")
    validate_uploaded_file_required_extension(upload, ["txt"])


def test_validate_uploaded_file_required_extension_extension_fails_file_if_its_extension_is_not_on_extensions_list():
    upload = SimpleUploadedFile("test.txt", b"test", content_type="text/plain")
    with pytest.raises(ValidationError):
        validate_uploaded_file_required_extension(upload, ["pdf"])


def test_validate_uploaded_file_disallowed_extension_does_nothing_if_extensions_list_is_empty():
    upload = SimpleUploadedFile("test.txt", b"test", content_type="text/plain")
    validate_uploaded_file_disallowed_extension(upload, [])


def test_validate_uploaded_file_disallowed_extension_passes_file_if_its_extension_is_not_on_extensions_list():
    upload = SimpleUploadedFile("test.txt", b"test", content_type="text/plain")
    validate_uploaded_file_disallowed_extension(upload, ["pdf"])


def test_validate_uploaded_file_disallowed_extension_fails_file_if_its_extension_is_on_extensions_list():
    upload = SimpleUploadedFile("test.txt", b"test", content_type="text/plain")
    with pytest.raises(ValidationError):
        validate_uploaded_file_disallowed_extension(upload, ["txt"])
