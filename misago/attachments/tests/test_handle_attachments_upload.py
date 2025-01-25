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
