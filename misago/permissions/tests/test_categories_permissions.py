import pytest
from django.core.exceptions import PermissionDenied
from django.http import Http404

from ...categories.models import Category
from ...testutils import grant_category_group_permissions
from ..categories import (
    PermissionDenied,
    check_browse_category_permission,
    check_see_category_permission,
)
from ..enums import CategoryPermission
from ..proxy import UserPermissionsProxy


def test_check_see_category_permission_passes_if_user_has_permission(
    user, root_category, cache_versions
):
    category = Category(name="Category", slug="category")
    category.insert_at(root_category, position="last-child", save=True)

    grant_category_group_permissions(category, user.group, CategoryPermission.SEE)

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_category_permission(permissions, category)


def test_check_see_category_permission_fails_if_user_has_no_permission(
    user, root_category, cache_versions
):
    category = Category(name="Category", slug="category")
    category.insert_at(root_category, position="last-child", save=True)

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_category_permission(permissions, category)


def test_check_see_category_permission_passes_if_user_can_browse_parent_category(
    user, root_category, cache_versions
):
    parent_category = Category(name="Category", slug="category")
    parent_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(parent_category, position="last-child", save=True)

    grant_category_group_permissions(
        parent_category, user.group, CategoryPermission.SEE, CategoryPermission.BROWSE
    )
    grant_category_group_permissions(child_category, user.group, CategoryPermission.SEE)

    permissions = UserPermissionsProxy(user, cache_versions)

    check_see_category_permission(permissions, child_category)


def test_check_see_category_permission_passes_if_user_can_browse_parent_category_with_delay(
    user, root_category, cache_versions
):
    parent_category = Category(
        name="Category", slug="category", delay_browse_check=True
    )
    parent_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(parent_category, position="last-child", save=True)

    grant_category_group_permissions(
        parent_category, user.group, CategoryPermission.SEE
    )
    grant_category_group_permissions(child_category, user.group, CategoryPermission.SEE)

    permissions = UserPermissionsProxy(user, cache_versions)

    check_see_category_permission(permissions, child_category)


def test_check_see_category_permission_fails_if_user_cant_browse_parent_category(
    user, root_category, cache_versions
):
    parent_category = Category(
        name="Category", slug="category", delay_browse_check=True
    )
    parent_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(parent_category, position="last-child", save=True)

    grant_category_group_permissions(child_category, user.group, CategoryPermission.SEE)

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_category_permission(permissions, child_category)


def test_check_browse_category_permission_passes_if_user_has_see_and_browse_permissions(
    user, root_category, cache_versions
):
    category = Category(name="Category", slug="category")
    category.insert_at(root_category, position="last-child", save=True)

    grant_category_group_permissions(
        category, user.group, CategoryPermission.SEE, CategoryPermission.BROWSE
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    check_browse_category_permission(permissions, category)


def test_check_browse_category_permission_fails_if_user_has_no_permissions(
    user, root_category, cache_versions
):
    category = Category(name="Category", slug="category")
    category.insert_at(root_category, position="last-child", save=True)

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_browse_category_permission(permissions, category)


def test_check_browse_category_permission_fails_if_user_has_no_browse_permission(
    user, root_category, cache_versions
):
    category = Category(name="Category", slug="category")
    category.insert_at(root_category, position="last-child", save=True)

    grant_category_group_permissions(category, user.group, CategoryPermission.SEE)

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_browse_category_permission(permissions, category)


def test_check_browse_category_permission_fails_if_user_has_only_browse_permission(
    user, root_category, cache_versions
):
    category = Category(name="Category", slug="category")
    category.insert_at(root_category, position="last-child", save=True)

    grant_category_group_permissions(category, user.group, CategoryPermission.BROWSE)

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_browse_category_permission(permissions, category)


def test_check_browse_category_permission_passes_if_user_can_browse_parent_category(
    user, root_category, cache_versions
):
    parent_category = Category(name="Category", slug="category")
    parent_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(parent_category, position="last-child", save=True)

    grant_category_group_permissions(
        parent_category, user.group, CategoryPermission.SEE, CategoryPermission.BROWSE
    )
    grant_category_group_permissions(
        child_category, user.group, CategoryPermission.SEE, CategoryPermission.BROWSE
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    check_see_category_permission(permissions, child_category)


def test_check_browse_category_permission_passes_if_user_can_browse_parent_category_with_delay(
    user, root_category, cache_versions
):
    parent_category = Category(
        name="Category", slug="category", delay_browse_check=True
    )
    parent_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(parent_category, position="last-child", save=True)

    grant_category_group_permissions(
        parent_category, user.group, CategoryPermission.SEE
    )
    grant_category_group_permissions(
        child_category, user.group, CategoryPermission.SEE, CategoryPermission.BROWSE
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    check_see_category_permission(permissions, child_category)


def test_check_browse_category_permission_fails_if_user_cant_see_parent(
    user, root_category, cache_versions
):
    parent_category = Category(name="Category", slug="category")
    parent_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(parent_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category, user.group, CategoryPermission.SEE, CategoryPermission.BROWSE
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_category_permission(permissions, child_category)


def test_check_browse_category_permission_fails_if_user_cant_see_parent(
    user, root_category, cache_versions
):
    parent_category = Category(name="Category", slug="category")
    parent_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(parent_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category, user.group, CategoryPermission.SEE, CategoryPermission.BROWSE
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_category_permission(permissions, child_category)


def test_check_browse_category_permission_fails_if_user_cant_browse_parent(
    user, root_category, cache_versions
):
    parent_category = Category(name="Category", slug="category")
    parent_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(parent_category, position="last-child", save=True)

    grant_category_group_permissions(
        parent_category, user.group, CategoryPermission.SEE
    )
    grant_category_group_permissions(
        child_category, user.group, CategoryPermission.SEE, CategoryPermission.BROWSE
    )

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_category_permission(permissions, child_category)
