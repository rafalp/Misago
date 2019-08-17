from unittest.mock import Mock

import pytest

from ..user import get_or_create_user, user_needs_updating

SSO_ID = 1


@pytest.fixture
def sso_user(user):
    user.sso_id = SSO_ID
    user.save()
    return user


def test_new_user_is_created_if_user_with_given_sso_id_doesnt_exist(dynamic_settings):
    user = get_or_create_user(
        Mock(settings=dynamic_settings),
        {
            "id": SSO_ID,
            "username": "SsoUser",
            "email": "ssouser@example.com",
            "is_active": False,
        },
    )

    assert user.sso_id == SSO_ID
    assert user.username == "SsoUser"
    assert user.email == "ssouser@example.com"
    assert user.is_active is False


def test_user_with_sso_id_is_returned_if_they_exist(dynamic_settings, sso_user):
    user = get_or_create_user(
        Mock(settings=dynamic_settings),
        {"id": SSO_ID, "username": "SsoUser", "email": "ssouser@example.com"},
    )

    assert user == sso_user


def test_user_with_sso_id_is_updated_using_provider_data(dynamic_settings, sso_user):
    user = get_or_create_user(
        Mock(settings=dynamic_settings),
        {
            "id": SSO_ID,
            "username": "SsoUser",
            "email": "ssouser@example.com",
            "is_active": False,
        },
    )

    sso_user.refresh_from_db()
    assert sso_user.username == "SsoUser"
    assert sso_user.email == "ssouser@example.com"
    assert sso_user.is_active is False


def test_user_needs_updating_if_their_username_changed(user):
    assert user_needs_updating(user, {"username": "Changed", "email": user.email})


def test_user_needs_updating_if_their_email_changed(user):
    assert user_needs_updating(
        user, {"username": user.username, "email": "changed@example.com"}
    )


def test_user_needs_updating_if_their_active_status_changed(user):
    assert user_needs_updating(
        user,
        {
            "username": user.username,
            "email": user.email,
            "is_active": not user.is_active,
        },
    )


def test_user_doesnt_need_updating_if_their_data_is_same(user):
    assert not user_needs_updating(
        user,
        {"username": user.username, "email": user.email, "is_active": user.is_active},
    )
