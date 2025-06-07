import pytest
from django.core.exceptions import PermissionDenied

from ..notifications import check_notifications_permission
from ..proxy import UserPermissionsProxy


def test_check_notifications_permission_passes_authenticated_user(user, cache_versions):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_notifications_permission(permissions)


def test_check_notifications_permission_fails_if_user_is_anonymous(
    anonymous_user, cache_versions
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_notifications_permission(permissions)
