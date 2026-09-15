import pytest
from django.core.exceptions import PermissionDenied

from ..search import check_search_permission


def test_check_search_permission_passes_user_with_permission(
    user_permissions_factory, user, members_group
):
    members_group.can_search = True
    members_group.save()

    permissions = user_permissions_factory(user)
    check_search_permission(permissions)


def test_check_search_permission_fails_user_without_permission(
    user_permissions_factory, user, members_group
):
    members_group.can_search = False
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_search_permission(permissions)
