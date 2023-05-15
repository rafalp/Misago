from typing import List

from django.core.cache import cache
from django.urls import reverse

from ..acl import ACL_CACHE
from ..users.models import AnonymousUser
from .models import Category

CACHE_NAME = "categories_map"


def get_categories_map(request) -> List[dict]:
    cache_key = get_cache_key(request)
    categories_map = cache.get(cache_key, None)
    if categories_map is None:
        categories_map = get_categories_map_from_db(request)
        cache.set(cache_key, categories_map)
    return categories_map


def get_cache_key(request) -> str:
    acl_version = request.cache_versions[ACL_CACHE]
    if request.user.is_authenticated:
        user_acl_key = request.user.acl_key
    else:
        user_acl_key = AnonymousUser.acl_key

    return f"{CACHE_NAME}:{acl_version}:{user_acl_key}"


MAP_CATEGORY_FIELDS = (
    "id",
    "name",
    "slug",
    "short_name",
    "color",
    "level",
)


def get_categories_map_from_db(request) -> List[dict]:
    categories_list = []
    queryset = Category.objects.filter(
        id__in=request.user_acl["visible_categories"],
        level=1,
        special_role__isnull=True,
    ).order_by("lft")

    for category in queryset.values(*MAP_CATEGORY_FIELDS):
        category_url = reverse(
            "misago:category",
            kwargs={"pk": category["id"], "slug": category["slug"]},
        )

        category_json = {
            "id": category["id"],
            "name": category["name"],
            "shortName": category["short_name"],
            "color": category["color"],
            "url": category_url,
        }

        categories_list.append(category_json)

    return categories_list
