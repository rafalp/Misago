import pytest
from django.core.exceptions import PermissionDenied

from ..private_threads import check_private_threads_permission
from ..proxy import UserPermissionsProxy


def test_check_private_threads_permission_passes_if_user_has_permission(
    user, cache_versions
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_private_threads_permission(permissions)


def test_check_private_threads_permission_fails_if_user_has_no_permission(
    user, members_group, cache_versions
):
    members_group.can_use_private_threads = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_private_threads_permission(permissions)


def test_check_private_threads_permission_fails_if_user_is_anonymous(
    anonymous_user, cache_versions
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_private_threads_permission(permissions)
