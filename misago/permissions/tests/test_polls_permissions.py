import pytest
from django.core.exceptions import PermissionDenied

from ..polls import check_start_poll_permission
from ..proxy import UserPermissionsProxy


def test_check_start_poll_permission_allows_user_to_start_polls(user, cache_versions):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_start_poll_permission(permissions)


def test_check_start_poll_permission_fails_if_user_is_anonymous(
    anonymous_user, cache_versions
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_poll_permission(permissions)


def test_check_start_poll_permission_fails_if_user_has_no_permission_to_start_polls(
    user, members_group, cache_versions
):
    members_group.can_start_polls = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_poll_permission(permissions)
