import pytest
from django.core.exceptions import PermissionDenied
from django.http import Http404

from ..generic import check_access_category_permission
from ..enums import CategoryPermission
from ..models import CategoryGroupPermission
from ..proxy import UserPermissionsProxy


def test_check_access_category_permission_passes_user_with_permission_to_see_category(
    user, cache_versions, default_category
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_access_category_permission(permissions, default_category)


def test_check_access_category_permission_fails_user_without_category_permission(
    user, cache_versions, default_category
):
    CategoryGroupPermission.objects.filter(
        category=default_category, permission=CategoryPermission.SEE
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_access_category_permission(permissions, default_category)


def test_check_access_category_permission_passes_user_with_permission_to_use_private_threads(
    user, cache_versions, private_threads_category
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_access_category_permission(permissions, private_threads_category)


def test_check_access_category_permission_fails_user_without_private_threads_permission(
    user, members_group, cache_versions, private_threads_category
):
    members_group.can_use_private_threads = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_access_category_permission(permissions, private_threads_category)
