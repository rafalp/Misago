from typing import List

from django.core.cache import cache
from django.urls import reverse

from ..acl import ACL_CACHE
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
    return f"{CACHE_NAME}:{acl_version}:{request.user.acl_key}"


MAP_CATEGORY_FIELDS = (
    "id",
    "parent_id",
    "name",
    "slug",
    "short_name",
    "color",
    "level",
)


def get_categories_map_from_db(request) -> List[dict]:
    categories_list = []
    categories_dict = {}

    queryset = Category.objects.filter(
        id__in=request.user_acl["browseable_categories"],
    ).order_by("lft")

    for category in queryset.values(*MAP_CATEGORY_FIELDS):
        parent_id = category["parent_id"]
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

        if category["level"] > 1 and parent_id:
            categories_dict[parent_id]["children"].append(category_json)
        else:
            category_json["children"] = []
            categories_list.append(category_json)
            categories_dict[category_json["id"]] = category_json

    return categories_list
