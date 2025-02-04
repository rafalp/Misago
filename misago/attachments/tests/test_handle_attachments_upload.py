import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from ...permissions.proxy import UserPermissionsProxy
from ...conf.test import override_dynamic_settings
from ..enums import AttachmentTypeRestriction
from ..upload import handle_attachments_upload


def test_handle_attachments_upload_stores_uploaded_files(
    rf, user, dynamic_settings, cache_versions, teardown_attachments
):
    request = rf.post("/upload/")
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    attachments, error = handle_attachments_upload(
        request, [SimpleUploadedFile("test.txt", b"Hello world!", "text/plain")]
    )

    assert not error

    assert len(attachments) == 1
    attachment = attachments[0]
    assert attachment.filetype_id == "txt"
    assert attachment.name == "test.txt"
    assert attachment.uploader == user


def test_handle_attachments_upload_validates_uploaded_files(
    rf, user, dynamic_settings, cache_versions, teardown_attachments
):
    request = rf.post("/upload/")
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    attachments, error = handle_attachments_upload(
        request, [SimpleUploadedFile("test.txt", b"Hello world!", "text/invalid")]
    )

    assert error
    assert error.messages == ["test.txt: uploaded file type is not allowed."]

    assert not attachments


def test_handle_attachments_upload_stores_valid_uploads_on_upload_errors(
    rf, user, dynamic_settings, cache_versions, teardown_attachments
):
    request = rf.post("/upload/")
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    attachments, error = handle_attachments_upload(
        request,
        [
            SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            SimpleUploadedFile("invalid.txt", b"Hello world!", "text/invalid"),
        ],
    )

    assert error
    assert error.messages == ["invalid.txt: uploaded file type is not allowed."]

    assert len(attachments) == 1
    attachment = attachments[0]
    assert attachment.filetype_id == "txt"
    assert attachment.name == "test.txt"
    assert attachment.uploader == user


@override_dynamic_settings(
    restrict_attachments_extensions="txt",
    restrict_attachments_extensions_type=AttachmentTypeRestriction.REQUIRE.value,
)
def test_handle_attachments_upload_validates_allowed_uploaded_files_extensions_if_list_is_set(
    rf, user, dynamic_settings, cache_versions, teardown_attachments
):
    request = rf.post("/upload/")
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    attachments, error = handle_attachments_upload(
        request,
        [
            SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            SimpleUploadedFile("test.pdf", b"Hello world!", "application/pdf"),
        ],
    )

    assert error
    assert error.messages == ["test.pdf: uploaded file type is not allowed."]

    assert len(attachments) == 1
    attachment = attachments[0]
    assert attachment.filetype_id == "txt"
    assert attachment.name == "test.txt"
    assert attachment.uploader == user


@override_dynamic_settings(
    restrict_attachments_extensions="pdf",
    restrict_attachments_extensions_type=AttachmentTypeRestriction.DISALLOW.value,
)
def test_handle_attachments_upload_validates_disallowed_uploaded_files_extensions_if_list_is_set(
    rf, user, dynamic_settings, cache_versions, teardown_attachments
):
    request = rf.post("/upload/")
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    attachments, error = handle_attachments_upload(
        request,
        [
            SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            SimpleUploadedFile("test.pdf", b"Hello world!", "application/pdf"),
        ],
    )

    assert error
    assert error.messages == ["test.pdf: uploaded file type is not allowed."]

    assert len(attachments) == 1
    attachment = attachments[0]
    assert attachment.filetype_id == "txt"
    assert attachment.name == "test.txt"
    assert attachment.uploader == user


class SimpleUploadedFileWithForcedSize(SimpleUploadedFile):
    def __init__(self, *args, size: int):
        super().__init__(*args)
        self.size: int = size


def test_handle_attachments_upload_validates_attachments_storage(
    rf, user, members_group, dynamic_settings, cache_versions, teardown_attachments
):
    members_group.unused_attachments_storage_limit = 1
    members_group.save()

    request = rf.post("/upload/")
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    attachments, error = handle_attachments_upload(
        request,
        [
            SimpleUploadedFileWithForcedSize(
                "test.txt",
                b"Hello world!",
                "text/plain",
                size=5 * 1024 * 1024,
            ),
        ],
    )

    assert error
    assert error.messages == [
        "test.txt: uploaded file exceeds your remaining attachment space (1.0\xa0MB).",
    ]

    assert not attachments


def test_handle_attachments_upload_validates_storage_for_multiple_uploads(
    rf, user, members_group, dynamic_settings, cache_versions, teardown_attachments
):
    members_group.unused_attachments_storage_limit = 1
    members_group.save()

    request = rf.post("/upload/")
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    attachments, error = handle_attachments_upload(
        request,
        [
            SimpleUploadedFileWithForcedSize(
                "test.txt",
                b"Hello world!",
                "text/plain",
                size=1000 * 1024,
            ),
            SimpleUploadedFileWithForcedSize(
                "test2.txt",
                b"Hello world!",
                "text/plain",
                size=1024 * 1024,
            ),
        ],
    )

    assert error
    assert error.messages == [
        "test2.txt: uploaded file exceeds your remaining attachment space (24.0\xa0KB).",
    ]

    assert len(attachments) == 1
    attachment = attachments[0]
    assert attachment.filetype_id == "txt"
    assert attachment.name == "test.txt"
    assert attachment.uploader == user


def test_handle_attachments_upload_annotates_attachments_with_keys_if_they_are_used(
    rf, user, dynamic_settings, cache_versions, teardown_attachments
):
    request = rf.post("/upload/")
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    attachments, error = handle_attachments_upload(
        request,
        [
            SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            SimpleUploadedFile("test2.txt", b"Hello world!", "text/plain"),
        ],
        ["key1", "key2"],
    )

    assert not error

    assert len(attachments) == 2
    attachment = attachments[0]
    assert attachment.filetype_id == "txt"
    assert attachment.name == "test.txt"
    assert attachment.uploader == user
    assert attachment.upload_key == "key1"

    attachment2 = attachments[1]
    assert attachment2.filetype_id == "txt"
    assert attachment2.name == "test2.txt"
    assert attachment2.uploader == user
    assert attachment2.upload_key == "key2"


def test_handle_attachments_upload_raises_validation_error_if_keys_is_empty_list(
    rf, user, dynamic_settings, cache_versions, teardown_attachments
):
    request = rf.post("/upload/")
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(ValidationError) as exc_info:
        handle_attachments_upload(
            request,
            [SimpleUploadedFile("test.txt", b"Hello world!", "text/plain")],
            [],
        )

    assert exc_info.value.messages == ["'keys' and 'uploads' must have same length"]
    assert exc_info.value.code == "upload_handler"


def test_handle_attachments_upload_raises_validation_error_if_there_are_more_keys_than_uploads(
    rf, user, dynamic_settings, cache_versions, teardown_attachments
):
    request = rf.post("/upload/")
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(ValidationError) as exc_info:
        handle_attachments_upload(
            request,
            [SimpleUploadedFile("test.txt", b"Hello world!", "text/plain")],
            ["key1", "key2"],
        )

    assert exc_info.value.messages == ["'keys' and 'uploads' must have same length"]
    assert exc_info.value.code == "upload_handler"


def test_handle_attachments_upload_raises_validation_error_if_there_duplicated_keys(
    rf, user, dynamic_settings, cache_versions, teardown_attachments
):
    request = rf.post("/upload/")
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(ValidationError) as exc_info:
        handle_attachments_upload(
            request,
            [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
                SimpleUploadedFile("test2.txt", b"Hello world!", "text/plain"),
            ],
            ["key1", "key1"],
        )

    assert exc_info.value.messages == ["'keys' must be unique"]
    assert exc_info.value.code == "upload_handler"


def test_handle_attachments_upload_raises_validation_error_if_there_are_less_keys_than_uploads(
    rf, user, dynamic_settings, cache_versions, teardown_attachments
):
    request = rf.post("/upload/")
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(ValidationError) as exc_info:
        handle_attachments_upload(
            request,
            [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
                SimpleUploadedFile("test2.txt", b"Hello world!", "text/plain"),
            ],
            ["key1"],
        )

    assert exc_info.value.messages == ["'keys' and 'uploads' must have same length"]
    assert exc_info.value.code == "upload_handler"


def test_handle_attachments_upload_returns_validation_errors_dict_if_keys_are_used(
    rf, user, dynamic_settings, cache_versions, teardown_attachments
):
    request = rf.post("/upload/")
    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    attachments, error = handle_attachments_upload(
        request,
        [
            SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            SimpleUploadedFile("test2.txt", b"Hello world!", "text/invalid"),
            SimpleUploadedFile("test3.txt", b"Hello world!", "text/plain"),
        ],
        ["key1", "key2", "key3"],
    )

    assert error
    assert error.message_dict == {
        "key2": ["test2.txt: uploaded file type is not allowed."],
    }

    assert len(attachments) == 2
    attachment = attachments[0]
    assert attachment.filetype_id == "txt"
    assert attachment.name == "test.txt"
    assert attachment.uploader == user
    assert attachment.upload_key == "key1"

    attachment2 = attachments[1]
    assert attachment2.filetype_id == "txt"
    assert attachment2.name == "test3.txt"
    assert attachment2.uploader == user
    assert attachment2.upload_key == "key3"
