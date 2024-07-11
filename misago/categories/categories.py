from typing import Any

from django.core.cache import cache
from django.urls import reverse

from ..cache.enums import CacheName
from ..permissions.enums import CategoryPermission
from ..permissions.proxy import UserPermissionsProxy
from .hooks import (
    get_categories_query_values_hook,
    get_category_data_hook,
)
from .models import Category

CACHE_PREFIX = "categories"


def get_categories(
    user_permissions: UserPermissionsProxy,
    cache_versions: dict[str, str],
) -> dict[int, dict]:
    cache_key = get_cache_key(user_permissions, cache_versions)
    categories_map = cache.get(cache_key, None)
    if categories_map is None:
        categories_map = get_categories_from_db(user_permissions)
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


def get_categories_from_db(user_permissions: UserPermissionsProxy) -> list[dict]:
    categories_list = []
    queryset = Category.objects.filter(
        id__in=user_permissions.categories[CategoryPermission.SEE],
        special_role__isnull=True,
    ).order_by("lft")

    fields = get_category_fields()
    for category in queryset.values(*fields):
        categories_list.append(get_category_data(category))

    return categories_list


CATEGORY_FIELDS = (
    "id",
    "parent_id",
    "name",
    "slug",
    "short_name",
    "color",
    "css_class",
    "delay_browse_check",
    "show_started_only",
    "is_closed",
    "is_vanilla",
    "level",
    "lft",
    "rght",
)


def get_category_fields() -> set[str]:
    return get_categories_query_values_hook(_get_category_fields_action)


def _get_category_fields_action() -> set[str]:
    return set(CATEGORY_FIELDS)


def get_category_data(result: dict[str, Any]) -> dict[str, Any]:
    return get_category_data_hook(_get_category_data_action, result)


def _get_category_data_action(result: dict[str, Any]) -> dict[str, Any]:
    category_url = reverse(
        "misago:category",
        kwargs={"id": result["id"], "slug": result["slug"]},
    )

    return {
        "id": result["id"],
        "parent_id": result["parent_id"] if result["level"] > 1 else None,
        "name": result["name"],
        "short_name": result["short_name"],
        "color": result["color"],
        "css_class": result["css_class"],
        "delay_browse_check": result["delay_browse_check"],
        "show_started_only": result["show_started_only"],
        "is_closed": result["is_closed"],
        "is_vanilla": result["is_vanilla"],
        "level": result["level"] - 1,
        "lft": result["lft"],
        "rght": result["rght"],
        "url": category_url,
    }
