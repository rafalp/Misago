import pytest
from django.core.exceptions import PermissionDenied

from ..accounts import check_delete_own_account_permission


def test_regular_user_can_delete_their_own_account(user):
    check_delete_own_account_permission(user)


def test_django_staff_cant_delete_their_own_account(staffuser):
    with pytest.raises(PermissionDenied):
        check_delete_own_account_permission(staffuser)


def test_misago_admin_cant_delete_their_own_account(admin):
    with pytest.raises(PermissionDenied):
        check_delete_own_account_permission(admin)


def test_misago_root_cant_delete_their_own_account(root_admin):
    with pytest.raises(PermissionDenied):
        check_delete_own_account_permission(root_admin)
