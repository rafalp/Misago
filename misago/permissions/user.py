from django.contrib.auth import get_user_model
from django.core.cache import cache

from ..cache.enums import CacheName
from ..categories.enums import CategoryTree
from ..categories.models import Category
from ..users.models import Group
from .hooks import build_user_permissions_hook

User = get_user_model()


def get_user_permissions(user: User, cache_versions: dict) -> dict:
    cache_key = get_user_permissions_cache_key(user, cache_versions)
    permissions = cache.get(cache_key)

    if permissions is None:
        permissions = build_user_permissions(user)
        cache.set(cache_key, permissions)

    return permissions


def get_user_permissions_cache_key(user: User, cache_versions: dict) -> str:
    return ":".join(
        (
            user.permissions_id,
            cache_versions[CacheName.PERMISSIONS],
            cache_versions[CacheName.MODERATORS],
        )
    )


def build_user_permissions(user: User) -> dict:
    groups: list[Group] = list(Group.objects.filter(id__in=user.groups_ids))
    permissions = build_user_permissions_hook(_build_user_permissions_action, groups)

    permissions["category"] = build_user_category_permissions(groups, permissions)

    return permissions


def _build_user_permissions_action(groups: list[Group]) -> dict:
    permissions = {"category": {}}
    return permissions


def build_user_category_permissions(groups: list[Group], permissions: dict) -> dict:
    categories: dict[int, Category] = {
        category.id: category
        for category in Category.objects.filter(
            tree_id=CategoryTree.THREADS,
            level__gt=0,
        )
    }

    return _build_user_category_permissions_action(groups, categories, permissions)


def _build_user_category_permissions_action(
    user: User,
    groups: list[Group],
    categories: dict[int, Category],
    permissions: dict,
) -> dict:
    category_permissions = {}
    return category_permissions
