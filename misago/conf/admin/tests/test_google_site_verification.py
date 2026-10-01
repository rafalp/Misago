from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ...models import Setting

admin_link = reverse("misago:admin:settings:analytics:index")


@pytest.fixture
def setting(db):
    return Setting.objects.get(setting="google_site_verification")


@pytest.fixture
def setting_with_value(setting):
    setting.dry_value = "asdfghjkl1234567"
    setting.save()
    return setting


def test_site_verification_cant_be_edited_directly(admin_client, setting):
    admin_client.post(admin_link, {"google_site_verification": "test"})
    setting.refresh_from_db()
    assert not setting.value


def test_site_verification_is_set_from_uploaded_file(admin_client, setting):
    verification = b"google-site-verification: googleasdfghjkl1234567.html"
    verification_file = SimpleUploadedFile("test.html", verification, "text/html")
    admin_client.post(admin_link, {"google_site_verification_file": verification_file})

    setting.refresh_from_db()
    assert setting.value == "asdfghjkl1234567"


def test_non_html_uploaded_file_is_rejected(admin_client, setting):
    verification_file = SimpleUploadedFile("test.html", b"test", "text/plain")
    admin_client.post(admin_link, {"google_site_verification_file": verification_file})

    setting.refresh_from_db()
    assert not setting.value


def test_empty_uploaded_file_is_rejected(admin_client, setting_with_value):
    verification_file = SimpleUploadedFile("test.html", b"", "text/html")
    admin_client.post(admin_link, {"google_site_verification_file": verification_file})

    setting_with_value.refresh_from_db()
    assert setting_with_value.value


def test_incorrect_uploaded_file_is_rejected(admin_client, setting_with_value):
    verification = b"google-site-verification: google.html"
    verification_file = SimpleUploadedFile("test.html", verification, "text/html")
    admin_client.post(admin_link, {"google_site_verification_file": verification_file})

    setting_with_value.refresh_from_db()
    assert setting_with_value.value


def test_uploaded_file_is_opened_and_closed(admin_client):
    from django.core.files.uploadedfile import InMemoryUploadedFile

    verification = b"google-site-verification: google.html"
    verification_file = SimpleUploadedFile("test.html", verification, "text/html")

    upload_open = InMemoryUploadedFile.open
    upload_close = InMemoryUploadedFile.close

    with (
        patch.object(
            InMemoryUploadedFile, "open", side_effect=upload_open, autospec=True
        ) as mock_open_file,
        patch.object(
            InMemoryUploadedFile, "close", side_effect=upload_close, autospec=True
        ) as mock_close_file,
    ):
        admin_client.post(
            admin_link, {"google_site_verification_file": verification_file}
        )

    mock_open_file.assert_called_once()
    assert mock_close_file.call_count == 2
