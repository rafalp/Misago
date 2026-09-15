from typing import Any

from django.core.cache import cache

from ..cache.enums import CacheName
from ..permissions.enums import CategoryPermission
from ..permissions.proxy import UserPermissionsProxy
from .hooks import serialize_category_data_hook
from .models import Category

CACHE_PREFIX = "categories"

CATEGORY_FIELDS = (
    "id",
    "parent_id",
    "level",
    "lft",
    "rght",
    "name",
    "slug",
    "short_name",
    "color",
    "css_class",
    "delay_browse_check",
    "show_started_only",
    "is_vanilla",
    "plugin_data",
)


def get_categories_data(
    user_permissions: UserPermissionsProxy,
    cache_versions: dict[str, str],
) -> dict[int, dict]:
    cache_key = get_cache_key(user_permissions, cache_versions)
    categories_map = cache.get(cache_key, None)
    if categories_map is None:
        categories_map = get_categories_data_from_db(user_permissions)
        cache.set(cache_key, categories_map)
    return {c["id"]: c for c in categories_map}


def get_cache_key(
    user_permissions: UserPermissionsProxy,
    cache_versions: dict[str, str],
) -> str:
    categories_version = cache_versions[CacheName.CATEGORIES]
    perms_version = cache_versions[CacheName.PERMISSIONS]

    if user_permissions.user.is_authenticated:
        permissions_id = user_permissions.user.permissions_id
    else:
        permissions_id = "anonymous"

    return f"{CACHE_PREFIX}:{categories_version}:{perms_version}:{permissions_id}"


def get_categories_data_from_db(user_permissions: UserPermissionsProxy) -> list[dict]:
    categories_list = []
    queryset = Category.objects.filter(
        id__in=user_permissions.categories[CategoryPermission.SEE],
        special_role__isnull=True,
    ).order_by("lft")

    for category in queryset.values(*CATEGORY_FIELDS):
        categories_list.append(serialize_category_data(category))

    return categories_list


def serialize_category_data(result: dict[str, Any]) -> dict[str, Any]:
    return serialize_category_data_hook(_serialize_category_data_action, result)


def _serialize_category_data_action(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": result["id"],
        "parent_id": result["parent_id"] if result["level"] > 1 else None,
        "level": result["level"] - 1,
        "lft": result["lft"],
        "rght": result["rght"],
        "name": result["name"],
        "slug": result["slug"],
        "short_name": result["short_name"],
        "color": result["color"],
        "css_class": result["css_class"],
        "delay_browse_check": result["delay_browse_check"],
        "show_started_only": result["show_started_only"],
        "is_vanilla": result["is_vanilla"],
        "plugin_data": {},
    }
