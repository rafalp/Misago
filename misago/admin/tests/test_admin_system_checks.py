from datetime import timedelta
from unittest.mock import Mock

import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ...test import assert_contains
from ...users.datadownloads import request_user_data_download
from ...users.models import DataDownload
from ...users.test import create_test_user
from ..views.index import (
    check_cache,
    check_data_downloads,
    check_debug_status,
    check_forum_address,
    check_https,
    check_inactive_users,
)

User = get_user_model()

admin_link = reverse("misago:admin:index")


def test_cache_check_passess_if_cache_can_be_read_after_setting(mocker):
    mocker.patch("misago.admin.views.index.cache.set")
    mocker.patch("misago.admin.views.index.cache.get", return_value="ok")
    assert check_cache() == {"is_ok": True}


def test_cache_check_passess_if_cache_cant_be_read_after_setting(mocker):
    mocker.patch("misago.admin.views.index.cache.set")
    mocker.patch("misago.admin.views.index.cache.get", return_value=None)
    assert check_cache() == {"is_ok": False}


def test_warning_about_disabled_cache_is_displayed_on_checks_list(mocker, admin_client):
    mocker.patch("misago.admin.views.index.check_cache", return_value={"is_ok": False})
    response = admin_client.get(admin_link)
    assert_contains(response, "Cache is disabled")


def test_data_downloads_processing_check_passes_if_there_are_no_data_downloads(db):
    assert check_data_downloads() == {"is_ok": True, "count": 0}


def test_ready_data_downloads_are_excluded_by_check(user):
    data_download = request_user_data_download(user)
    data_download.status = DataDownload.STATUS_READY
    data_download.save()

    assert check_data_downloads() == {"is_ok": True, "count": 0}


def test_expired_data_downloads_are_excluded_by_check(user):
    data_download = request_user_data_download(user)
    data_download.status = DataDownload.STATUS_EXPIRED
    data_download.save()

    assert check_data_downloads() == {"is_ok": True, "count": 0}


def test_recent_pending_data_downloads_are_excluded_by_check(user):
    data_download = request_user_data_download(user)
    data_download.status = DataDownload.STATUS_PENDING
    data_download.save()

    assert check_data_downloads() == {"is_ok": True, "count": 0}


def test_recent_processing_data_downloads_are_excluded_by_check(user):
    data_download = request_user_data_download(user)
    data_download.status = DataDownload.STATUS_PROCESSING
    data_download.save()

    assert check_data_downloads() == {"is_ok": True, "count": 0}


def test_check_fails_if_there_are_old_processing_data_downloads(user):
    data_download = request_user_data_download(user)
    data_download.status = DataDownload.STATUS_PROCESSING
    data_download.requested_on = timezone.now() - timedelta(days=5)
    data_download.save()

    assert check_data_downloads() == {"is_ok": False, "count": 1}


def test_check_fails_if_there_are_old_pending_data_downloads(user):
    data_download = request_user_data_download(user)
    data_download.status = DataDownload.STATUS_PENDING
    data_download.requested_on = timezone.now() - timedelta(days=5)
    data_download.save()

    assert check_data_downloads() == {"is_ok": False, "count": 1}


def test_warning_about_unprocessed_data_downloads_is_displayed_on_checks_list(
    admin_client, user
):
    data_download = request_user_data_download(user)
    data_download.status = DataDownload.STATUS_PENDING
    data_download.requested_on = timezone.now() - timedelta(days=5)
    data_download.save()

    response = admin_client.get(admin_link)
    assert_contains(response, "There is 1 unprocessed data download request")


class RequestMock:
    absolute_uri = "https://misago-project.org/somewhere/"

    def __init__(self, settings):
        self.settings = settings

    def build_absolute_uri(self, location):
        assert location == "/"
        return self.absolute_uri


@pytest.fixture
def request_mock(dynamic_settings):
    return RequestMock(dynamic_settings)


incorrect_address = "http://somewhere.com"
correct_address = RequestMock.absolute_uri


@override_dynamic_settings(forum_address=None)
def test_forum_address_check_handles_setting_not_configured(request_mock):
    result = check_forum_address(request_mock)
    assert result == {
        "is_ok": False,
        "set_address": None,
        "correct_address": request_mock.absolute_uri,
    }


@override_dynamic_settings(forum_address=incorrect_address)
def test_forum_address_check_detects_invalid_address_configuration(request_mock):
    result = check_forum_address(request_mock)
    assert result == {
        "is_ok": False,
        "set_address": incorrect_address,
        "correct_address": request_mock.absolute_uri,
    }


@override_dynamic_settings(forum_address=correct_address)
def test_forum_address_check_detects_valid_address_configuration(request_mock):
    result = check_forum_address(request_mock)
    assert result == {
        "is_ok": True,
        "set_address": correct_address,
        "correct_address": request_mock.absolute_uri,
    }


@override_dynamic_settings(forum_address=None)
def test_warning_about_unset_forum_address_is_displayed_on_checks_list(admin_client):
    response = admin_client.get(admin_link)
    assert_contains(response, "address")


@override_dynamic_settings(forum_address=incorrect_address)
def test_warning_about_incorrect_forum_address_is_displayed_on_checks_list(
    admin_client
):
    response = admin_client.get(admin_link)
    assert_contains(response, "address")


@override_settings(DEBUG=False)
def test_debug_check_passess_if_debug_is_disabled():
    assert check_debug_status() == {"is_ok": True}


@override_settings(DEBUG=True)
def test_debug_check_fails_if_debug_is_enabled():
    assert check_debug_status() == {"is_ok": False}


@override_settings(DEBUG=True)
def test_warning_about_enabled_debug_is_displayed_on_checks_list(admin_client):
    response = admin_client.get(admin_link)
    assert_contains(response, "site is running in DEBUG mode")


def test_https_check_passes_if_site_is_accessed_over_https():
    request = Mock(is_secure=Mock(return_value=True))
    assert check_https(request) == {"is_ok": True}


def test_https_check_fails_if_site_is_accessed_without_https(mocker):
    request = Mock(is_secure=Mock(return_value=False))
    assert check_https(request) == {"is_ok": False}


def test_warning_about_accessing_site_without_https_is_displayed_on_checks_list(
    admin_client
):
    response = admin_client.get(admin_link)
    assert_contains(response, "site is not running over HTTPS")


def test_inactive_users_check_passess_if_there_are_no_inactive_users(db):
    assert check_inactive_users() == {"is_ok": True, "count": 0}


def test_inactive_users_check_passess_if_there_are_less_than_eleven_inactive_users(db):
    for i in range(10):
        create_test_user(
            "User%s" % i,
            "user%s@example.com" % i,
            requires_activation=User.ACTIVATION_USER,
        )
    assert check_inactive_users() == {"is_ok": True, "count": 10}


def test_inactive_users_check_fails_if_there_are_more_than_ten_inactive_users(db):
    for i in range(11):
        create_test_user(
            "User%s" % i,
            "user%s@example.com" % i,
            requires_activation=User.ACTIVATION_USER,
        )
    assert check_inactive_users() == {"is_ok": False, "count": 11}


def test_warning_about_inactive_users_is_displayed_on_checks_list(admin_client):
    for i in range(11):
        create_test_user(
            "User%s" % i,
            "user%s@example.com" % i,
            requires_activation=User.ACTIVATION_USER,
        )

    response = admin_client.get(admin_link)
    assert_contains(response, "There are 11 inactive users accounts")
