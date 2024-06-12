import pytest
from django.core.exceptions import PermissionDenied

from ..accounts import allow_delete_own_account


def test_allow_delete_own_account_raises_exception_if_user_is_misago_admin(admin):
    with pytest.raises(PermissionDenied):
        allow_delete_own_account(admin)


def test_allow_delete_own_account_raises_exception_if_user_is_django_admin(staffuser):
    with pytest.raises(PermissionDenied):
        allow_delete_own_account(staffuser)


def test_allow_delete_own_account_doesnt_raise_if_user_can_delete_own_account(user):
    allow_delete_own_account(user)
