from typing import TYPE_CHECKING, Union

from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache

from ..cache.enums import CacheName
from ..categories.enums import CategoryTree
from ..categories.models import Category
from ..users.enums import DefaultGroupId
from ..users.models import Group
from .enums import CategoryPermission
from .hooks import (
    build_user_category_permissions_hook,
    build_user_permissions_hook,
    get_user_permissions_hook,
)
from .models import CategoryGroupPermission
from .operations import (
    if_true,
    if_zero_or_greater,
)

if TYPE_CHECKING:
    from ..users.models import User


def get_user_permissions(
    user: Union["User", AnonymousUser], cache_versions: dict
) -> dict:
    return get_user_permissions_hook(_get_user_permissions_action, user, cache_versions)


def _get_user_permissions_action(
    user: Union["User", AnonymousUser], cache_versions: dict
) -> dict:
    cache_key = get_user_permissions_cache_key(user, cache_versions)
    permissions = cache.get(cache_key)

    if permissions is None:
        permissions = build_user_permissions(user)
        cache.set(cache_key, permissions)

    return permissions


def get_user_permissions_cache_key(
    user: Union["User", AnonymousUser], cache_versions: dict
) -> str:
    if user.is_anonymous:
        return f"anonymous:{cache_versions[CacheName.PERMISSIONS]}"

    return f"{user.permissions_id}:{cache_versions[CacheName.PERMISSIONS]}"


def build_user_permissions(user: Union["User", AnonymousUser]) -> dict:
    if user.is_anonymous:
        groups_ids = [DefaultGroupId.GUESTS]
    else:
        groups_ids = user.groups_ids

    groups: list[Group] = list(Group.objects.filter(id__in=groups_ids))
    permissions = build_user_permissions_hook(_build_user_permissions_action, groups)

    permissions["categories"] = build_user_category_permissions(groups, permissions)

    return permissions


def _build_user_permissions_action(groups: list[Group]) -> dict:
    permissions = {
        "can_change_username": False,
        "username_changes_limit": 0,
        "username_changes_expire": 0,
        "username_changes_span": 0,
        "can_see_user_profiles": False,
        "categories": {},
    }

    for group in groups:
        if_true(permissions, "can_change_username", group.can_change_username)
        if_zero_or_greater(
            permissions, "username_changes_limit", group.username_changes_limit
        )
        if_zero_or_greater(
            permissions, "username_changes_expire", group.username_changes_expire
        )
        if_zero_or_greater(
            permissions, "username_changes_span", group.username_changes_span
        )
        if_true(permissions, "can_see_user_profiles", group.can_see_user_profiles)

    return permissions


def build_user_category_permissions(groups: list[Group], permissions: dict) -> dict:
    categories: dict[int, Category] = {
        category.id: category
        for category in Category.objects.filter(
            tree_id=CategoryTree.THREADS,
            level__gt=0,
        )
    }

    category_permissions_queryset = CategoryGroupPermission.objects.filter(
        group__in=groups,
        category__in=categories.values(),
    ).values_list("category_id", "permission")

    category_permissions: dict[int, list[str]] = {}
    for category_id, permission in category_permissions_queryset:
        if category_id not in category_permissions:
            category_permissions[category_id] = []

        if permission not in category_permissions[category_id]:
            category_permissions[category_id].append(permission)

    return build_user_category_permissions_hook(
        _build_user_category_permissions_action,
        groups,
        categories,
        category_permissions,
        permissions,
    )


def _build_user_category_permissions_action(
    groups: list[Group],
    categories: dict[int, Category],
    category_permissions: dict[int, list[str]],
    user_permissions: dict,
) -> dict:
    permissions = {
        CategoryPermission.SEE: [],
        CategoryPermission.BROWSE: [],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }

    for category_id, category in categories.items():
        # Skip category if we can't see its parent
        if not can_see_parent_category(category, categories, permissions):
            continue

        # Skip category if we can't see it
        perms = category_permissions.get(category_id, [])
        if CategoryPermission.SEE not in perms:
            continue

        permissions[CategoryPermission.SEE].append(category_id)

        if CategoryPermission.BROWSE in perms:
            permissions[CategoryPermission.BROWSE].append(category_id)
        else:
            continue  # Skip rest of permissions if we can't read its contents

        if CategoryPermission.START in perms:
            permissions[CategoryPermission.START].append(category_id)
        if CategoryPermission.REPLY in perms:
            permissions[CategoryPermission.REPLY].append(category_id)
        if CategoryPermission.ATTACHMENTS in perms:
            permissions[CategoryPermission.ATTACHMENTS].append(category_id)

    return permissions


def can_see_parent_category(
    category: Category,
    categories: dict[int, Category],
    permissions: dict,
) -> bool:
    if category.level <= 1:
        return True

    if category.parent_id in permissions[CategoryPermission.BROWSE]:
        return True

    if category.parent_id in permissions[CategoryPermission.SEE]:
        return categories[category.parent_id].delay_browse_check

    return False
