import pytest
from django.urls import reverse

from ...attachments.models import Attachment
from ...test import assert_has_error_message


def test_attachment_is_deleted(admin_client, text_attachment):
    response = admin_client.post(
        reverse("misago:admin:attachments:delete", kwargs={"pk": text_attachment.id})
    )
    assert response.status_code == 302

    with pytest.raises(Attachment.DoesNotExist):
        text_attachment.refresh_from_db()


def test_non_existing_attachment_cant_be_deleted(admin_client):
    response = admin_client.post(
        reverse("misago:admin:attachments:delete", kwargs={"pk": 404})
    )
    assert_has_error_message(response, "Requested attachment does not exist.")
