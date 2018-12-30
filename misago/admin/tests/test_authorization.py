from time import time
from unittest.mock import Mock

import pytest
from django.test import override_settings

from ..auth import (
    TOKEN_KEY,
    UPDATED_KEY,
    authorize_admin,
    is_admin_authorized,
    remove_admin_authorization,
    update_admin_authorization,
)


@pytest.fixture
def admin_request(superuser):
    request = Mock(session={}, user=superuser)
    authorize_admin(request)
    return request


def test_authorizing_admin_updates_request_session(user):
    request = Mock(session={}, user=user)
    authorize_admin(request)
    assert request.session


def test_staff_user_can_be_authorized(staffuser):
    request = Mock(session={}, user=staffuser)
    authorize_admin(request)
    assert is_admin_authorized(request)


def test_non_staff_user_admin_authorization_is_never_valid(user):
    request = Mock(session={}, user=user)
    authorize_admin(request)
    assert not is_admin_authorized(request)


def test_anonymous_user_admin_authorization_is_never_valid(user, anonymous_user):
    request = Mock(session={}, user=user)
    authorize_admin(request)
    request.user = anonymous_user
    assert not is_admin_authorized(request)


def test_superuser_without_staff_flag_admin_authorization_is_never_valid(staffuser):
    request = Mock(session={}, user=staffuser)
    authorize_admin(request)
    request.user.is_staff = False
    assert not is_admin_authorized(request)


def test_admin_authorization_is_invalidated_by_user_pk_change(admin_request, superuser):
    admin_request.user.pk = superuser.pk + 1
    assert not is_admin_authorized(admin_request)


def test_admin_authorization_is_invalidated_by_user_email_change(admin_request):
    admin_request.user.email = "changed@example.com"
    assert not is_admin_authorized(admin_request)


def test_admin_authorization_is_invalidated_by_user_password_change(admin_request):
    admin_request.user.set_password("changed-password")
    assert not is_admin_authorized(admin_request)


def test_admin_authorization_is_invalidated_by_secret_key_change(admin_request):
    with override_settings(SECRET_KEY="changed-secret-key"):
        assert not is_admin_authorized(admin_request)


def test_admin_authorization_is_invalidated_by_token_change(admin_request):
    admin_request.session[TOKEN_KEY] = "authorization-token-changed"
    assert not is_admin_authorized(admin_request)


@override_settings(MISAGO_ADMIN_SESSION_EXPIRATION=5)
def test_admin_authorization_is_invalidated_by_token_expiration(admin_request):
    admin_request.session[UPDATED_KEY] = time() - 5 * 60 - 1
    assert not is_admin_authorized(admin_request)


def test_updating_authorization_extends_authorization_expiration_time(admin_request):
    admin_request.session[UPDATED_KEY] = 0
    update_admin_authorization(admin_request)
    assert admin_request.session[UPDATED_KEY]


def test_updating_authorization_validates_authorization(admin_request):
    admin_request.session[UPDATED_KEY] = 0
    update_admin_authorization(admin_request)
    assert is_admin_authorized(admin_request)


def test_removing_authorization_removes_autorization_from_request_session(
    admin_request
):
    admin_request.session[UPDATED_KEY] = 0
    remove_admin_authorization(admin_request)
    assert not admin_request.session


def test_removing_authorization_invalidates_autorization(admin_request):
    admin_request.session[UPDATED_KEY] = 0
    remove_admin_authorization(admin_request)
    assert not is_admin_authorized(admin_request)
