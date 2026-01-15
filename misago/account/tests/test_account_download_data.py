from unittest.mock import patch

from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...pagination.cursor import EmptyPageError
from ...test import (
    assert_contains,
    assert_has_success_message,
    assert_has_warning_message,
    assert_not_contains,
)
from ...users.datadownloads import request_user_data_download
from ...users.models import DataDownload


@override_dynamic_settings(allow_data_downloads=False)
def test_account_download_data_returns_error_if_data_downloads_are_disabled(db, client):
    response = client.get(reverse("misago:account-download-data"))
    assert response.status_code == 404


@override_dynamic_settings(allow_data_downloads=True)
def test_account_download_data_displays_login_required_page_to_anonymous_user(
    db, client
):
    response = client.get(reverse("misago:account-download-data"))
    assert_contains(response, "Sign in to change your settings", status_code=401)


@override_dynamic_settings(allow_data_downloads=True)
def test_account_download_data_renders_form(user_client):
    response = user_client.get(reverse("misago:account-download-data"))
    assert_contains(response, "Download your data")


@override_dynamic_settings(allow_data_downloads=True)
def test_account_download_data_renders_form_in_htmx(user_client):
    response = user_client.get(
        reverse("misago:account-download-data"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Download your data")


@override_dynamic_settings(allow_data_downloads=True)
def test_account_download_data_requests_new_download(user, user_client):
    response = user_client.post(reverse("misago:account-download-data"))
    assert response.status_code == 302
    assert_has_success_message(response, "Data download requested")

    DataDownload.objects.get(user=user, requester=user)


@override_dynamic_settings(allow_data_downloads=True)
def test_account_download_data_requests_new_download_in_htmx(user, user_client):
    response = user_client.post(
        reverse("misago:account-download-data"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Data download requested")
    assert_contains(response, "Preparing...")
    assert_not_contains(response, "You have no data downloads.")

    DataDownload.objects.get(user=user, requester=user)


@override_dynamic_settings(allow_data_downloads=True)
def test_account_download_data_displays_warning_on_multiple_download_requests(
    user, user_client
):
    download = request_user_data_download(user, user)

    response = user_client.post(reverse("misago:account-download-data"))
    assert response.status_code == 302
    assert_has_warning_message(
        response,
        "You can't request a new data download before the previous one completes.",
    )

    assert not DataDownload.objects.exclude(id=download.id).exists()


@override_dynamic_settings(allow_data_downloads=True)
def test_account_download_data_displays_warning_on_multiple_download_requests_in_htmx(
    user, user_client
):
    download = request_user_data_download(user, user)

    response = user_client.post(
        reverse("misago:account-download-data"),
        headers={"hx-request": "true"},
    )
    assert_contains(
        response,
        "You can&#x27;t request a new data download before the previous one completes.",
    )

    assert not DataDownload.objects.exclude(id=download.id).exists()


@override_dynamic_settings(allow_data_downloads=True)
def test_account_download_data_renders_pending_download_request(user, user_client):
    request_user_data_download(user, user)

    response = user_client.get(reverse("misago:account-download-data"))
    assert_contains(response, "Download your data")
    assert_contains(response, "Preparing...")
    assert_not_contains(response, "You have no data downloads.")


@override_dynamic_settings(allow_data_downloads=True)
def test_account_download_data_renders_processing_download_request(user, user_client):
    download = request_user_data_download(user, user)
    download.status = DataDownload.STATUS_PROCESSING
    download.save()

    response = user_client.get(reverse("misago:account-download-data"))
    assert_contains(response, "Download your data")
    assert_contains(response, "Preparing...")
    assert_not_contains(response, "You have no data downloads.")


@override_dynamic_settings(allow_data_downloads=True)
def test_account_download_data_renders_expired_download_request(user, user_client):
    download = request_user_data_download(user, user)
    download.status = DataDownload.STATUS_EXPIRED
    download.save()

    response = user_client.get(reverse("misago:account-download-data"))
    assert_contains(response, "Download your data")
    assert_contains(response, "Download expired")
    assert_not_contains(response, "You have no data downloads.")


@patch(
    "misago.account.views.settings.paginate_queryset", side_effect=EmptyPageError(10)
)
def test_account_download_data_redirects_to_last_page_for_invalid_cursor(
    mock_pagination, user_client, user
):
    response = user_client.get(reverse("misago:account-download-data"))

    assert response.status_code == 302
    assert (
        response["location"] == reverse("misago:account-download-data") + "?cursor=10"
    )

    mock_pagination.assert_called_once()
