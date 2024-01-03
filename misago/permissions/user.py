from django.contrib.auth import get_user_model
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

User = get_user_model()


def get_user_permissions(user: User | AnonymousUser, cache_versions: dict) -> dict:
    return get_user_permissions_hook(_get_user_permissions_action, user, cache_versions)


def _get_user_permissions_action(
    user: User | AnonymousUser, cache_versions: dict
) -> dict:
    cache_key = get_user_permissions_cache_key(user, cache_versions)
    permissions = cache.get(cache_key)

    if permissions is None:
        permissions = build_user_permissions(user)
        cache.set(cache_key, permissions)

    return permissions


def get_user_permissions_cache_key(
    user: User | AnonymousUser, cache_versions: dict
) -> str:
    if user.is_anonymous:
        return f"anonymous:{cache_versions[CacheName.PERMISSIONS]}"

    return f"{user.permissions_id}:{cache_versions[CacheName.PERMISSIONS]}"


def build_user_permissions(user: User | AnonymousUser) -> dict:
    if user.is_anonymous:
        groups_ids = [DefaultGroupId.GUESTS]
    else:
        groups_ids = user.groups_ids

    groups: list[Group] = list(Group.objects.filter(id__in=groups_ids))
    permissions = build_user_permissions_hook(_build_user_permissions_action, groups)

    permissions["category"] = build_user_category_permissions(groups, permissions)

    return permissions


def _build_user_permissions_action(groups: list[Group]) -> dict:
    permissions = {
        "user_profiles": False,
        "category": {},
    }

    for group in groups:
        if group.can_see_user_profiles:
            permissions["user_profiles"] = True

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
        category_permissions.setdefault(category_id, []).append(permission)

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
        if (
            category.level > 1
            and category.parent_id not in permissions[CategoryPermission.BROWSE]
        ):
            continue

        # Skip category if can't see it
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
