import pytest
from django.core.exceptions import PermissionDenied

from ..enums import CategoryPermission
from ..models import CategoryGroupPermission, Moderator
from ..proxy import UserPermissionsProxy
from ..threads import (
    check_post_in_closed_category_permission,
    check_start_thread_in_category_permission,
)


def test_check_post_in_closed_category_permission_passes_if_category_is_open(
    user, cache_versions, default_category
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_post_in_closed_category_permission(permissions, default_category)


def test_check_post_in_closed_category_permission_passes_if_user_is_global_moderator(
    moderator, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_post_in_closed_category_permission(permissions, default_category)


def test_check_post_in_closed_category_permission_passes_if_user_is_category_moderator(
    user, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = UserPermissionsProxy(user, cache_versions)
    check_post_in_closed_category_permission(permissions, default_category)


def test_check_post_in_closed_category_permission_fails_if_user_is_not_moderator(
    user, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_post_in_closed_category_permission(permissions, default_category)


def test_check_post_in_closed_category_permission_fails_if_user_is_anonymous(
    anonymous_user, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_post_in_closed_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_passes_if_user_has_permission(
    user, cache_versions, default_category
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_start_thread_in_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_passes_if_anonymous_has_permission(
    user, cache_versions, default_category
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_start_thread_in_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_fails_if_user_has_no_permission(
    user, cache_versions, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.START,
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_thread_in_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_fails_if_anonymous_has_no_permission(
    anonymous_user, guests_group, cache_versions, default_category
):
    CategoryGroupPermission.objects.filter(
        group=guests_group,
        permission=CategoryPermission.START,
    ).delete()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_thread_in_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_passes_if_user_is_global_moderator(
    moderator, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_start_thread_in_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_passes_if_user_is_category_moderator(
    user, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = UserPermissionsProxy(user, cache_versions)
    check_start_thread_in_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_fails_for_user_if_category_is_closed(
    user, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_thread_in_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_fails_for_anonymous_if_category_is_closed(
    anonymous_user, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_thread_in_category_permission(permissions, default_category)
