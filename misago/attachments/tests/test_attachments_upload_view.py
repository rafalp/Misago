import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...permissions.enums import CanUploadAttachments
from ..serialize import serialize_attachment

from ..enums import AllowedAttachments
from ..models import Attachment

upload_url = reverse("misago:attachments-upload")


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_attachments_upload_view_returns_error_if_new_uploads_are_disabled(db, client):
    response = client.post(upload_url)
    assert response.status_code == 403
    assert json.loads(response.content) == {
        "error": "Attachment uploads are disabled",
    }


def test_attachments_upload_view_returns_error_if_user_is_not_authenticated(db, client):
    response = client.post(upload_url)
    assert response.status_code == 403
    assert json.loads(response.content) == {
        "error": "Sign in to upload attachments",
    }


def test_attachments_upload_view_returns_error_if_user_has_no_upload_permission(
    members_group, user_client
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER.value
    members_group.save()

    response = user_client.post(upload_url)
    assert response.status_code == 403
    assert json.loads(response.content) == {
        "error": "You can't upload attachments",
    }


def test_attachments_upload_view_stores_uploaded_files(
    user, user_client, teardown_attachments
):
    response = user_client.post(
        upload_url,
        {
            "upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            ],
        },
    )
    assert response.status_code == 200

    attachment = Attachment.objects.first()
    assert attachment.id
    assert attachment.name == "test.txt"
    assert attachment.uploader == user

    assert json.loads(response.content) == {
        "errors": [],
        "attachments": [serialize_attachment(attachment)],
    }


def test_attachments_upload_view_validates_uploaded_files(
    user, user_client, teardown_attachments
):
    response = user_client.post(
        upload_url,
        {
            "upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/invalid"),
            ],
        },
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "errors": ["test.txt: uploaded file type is not allowed."],
        "attachments": [],
    }

    assert not Attachment.objects.exists()


def test_attachments_upload_view_stores_valid_uploads_on_upload_errors(
    user, user_client, teardown_attachments
):
    response = user_client.post(
        upload_url,
        {
            "upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
                SimpleUploadedFile("invalid.txt", b"Hello world!", "text/invalid"),
            ],
        },
    )
    assert response.status_code == 200

    attachment = Attachment.objects.first()
    assert attachment.id
    assert attachment.name == "test.txt"
    assert attachment.uploader == user

    assert json.loads(response.content) == {
        "errors": ["invalid.txt: uploaded file type is not allowed."],
        "attachments": [serialize_attachment(attachment)],
    }
