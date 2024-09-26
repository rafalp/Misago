from typing import TYPE_CHECKING, Union

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest

from ..permissions.enums import CategoryPermission
from ..permissions.proxy import UserPermissionsProxy
from ..readtracker.tracker import (
    annotate_categories_read_time,
    get_unread_categories,
)
from .enums import CategoryTree
from .models import Category

if TYPE_CHECKING:
    from ..users.models import User

__all__ = [
    "get_categories_data",
    "get_categories_page_component",
    "get_subcategories_data",
]


def get_categories_data(request: HttpRequest) -> list[dict]:
    permissions = request.user_permissions

    queryset = Category.objects.filter(
        id__in=permissions.categories[CategoryPermission.SEE],
        tree_id=CategoryTree.THREADS,
        level__gt=0,
    )

    queryset = annotate_categories_read_time(request.user, queryset)
    unread_categories = get_unread_categories(request, queryset)

    categories_data: dict[int, dict] = {
        category.id: get_category_data(
            category, category.id in unread_categories, permissions
        )
        for category in queryset
    }

    aggregate_categories_data(request, categories_data)

    return [
        category for category in categories_data.values() if show_top_category(category)
    ]


def show_top_category(category: dict) -> bool:
    if category["category"].level != 1:
        return False

    if category["category"].is_vanilla and not category["children"]:
        return False

    return True


def get_subcategories_data(request: HttpRequest, category: Category) -> list[dict]:
    if category.is_leaf_node():
        return []

    permissions = request.user_permissions

    queryset = Category.objects.filter(
        id__in=permissions.categories[CategoryPermission.SEE],
        tree_id=CategoryTree.THREADS,
        lft__gt=category.lft,
        rght__lt=category.rght,
    )

    queryset = annotate_categories_read_time(request.user, queryset)
    unread_categories = get_unread_categories(request, queryset)

    categories_data: dict[int, dict] = {
        category.id: get_category_data(
            category, category.id in unread_categories, permissions
        )
        for category in queryset
    }

    aggregate_categories_data(request, categories_data)

    return [
        subcategory
        for subcategory in categories_data.values()
        if subcategory["category"].parent_id == category.id
    ]


def get_category_data(
    category: Category, unread: bool, permissions: UserPermissionsProxy
) -> dict:
    if can_see_last_thread(category, permissions.user, permissions):
        category_last_thread = {
            "id": category.last_thread_id,
            "title": category.last_thread_title,
            "slug": category.last_thread_slug,
            "last_post_on": category.last_post_on,
            "last_poster": None,
            "last_poster_name": category.last_poster_name,
            "is_visible": (
                category.id in permissions.categories[CategoryPermission.BROWSE]
                or category.delay_browse_check
            ),
        }
    else:
        category_last_thread = None

    return {
        "category": category,
        "threads": category.threads,
        "posts": category.posts,
        "last_thread": category_last_thread,
        "unread": unread,
        "can_browse": (
            category.id in permissions.categories[CategoryPermission.BROWSE]
            or category.delay_browse_check
        ),
        "show_started_only": category.show_started_only,
        "children": [],
        "children_threads": category.threads,
        "children_posts": category.posts,
        "children_last_thread": category_last_thread,
        "children_unread": unread,
    }


def can_see_last_thread(
    category: Category,
    user: Union["User", AnonymousUser],
    permissions: UserPermissionsProxy,
) -> bool:
    if not category.last_thread_id:
        return False

    if (
        category.show_started_only
        and not permissions.is_category_moderator(category.id)
        and (user.is_anonymous or category.last_poster_id != user.id)
    ):
        return False

    return True


def aggregate_categories_data(
    request: HttpRequest,
    categories_data: dict[int, dict],
) -> None:
    last_posters = prefetch_last_posters(request, categories_data.values())

    # Populate categories last posters and read states
    # Aggregate categories to their parents
    for category_data in reversed(categories_data.values()):
        category = category_data["category"]

        # Populate last poster objects
        if category_data["last_thread"] and category.last_poster_id:
            last_poster = last_posters[category.last_poster_id]
            category_data["last_thread"].update(
                {
                    "last_poster": last_poster,
                    "last_poster_name": last_poster.username,
                }
            )

        # Aggregate data from category to its parent
        if category.parent_id in categories_data:
            parent = categories_data[category.parent_id]
            aggregate_category_to_its_parent(category_data, parent)


def aggregate_category_to_its_parent(category: dict, parent: dict):
    parent["children_threads"] += category["children_threads"]
    parent["children_posts"] += category["children_posts"]

    item_last_thread = category["children_last_thread"]
    parent_last_thread = parent["children_last_thread"]

    if (
        item_last_thread
        and item_last_thread["is_visible"]
        and (
            not parent_last_thread
            or item_last_thread["last_post_on"] > parent_last_thread["last_post_on"]
        )
    ):
        parent["children_last_thread"] = item_last_thread

    # Propagate to parent the new posts status
    if category["children_unread"]:
        parent["children_unread"] = True

    parent["children"].insert(0, category)


def prefetch_last_posters(
    request: HttpRequest, categories_list: list[dict]
) -> dict[int, "User"]:
    if not categories_list:
        return []

    last_posters: dict[int, User] = {}
    last_posters_ids: set[int] = set()
    for item in categories_list:
        last_poster_id = item["category"].last_poster_id
        if last_poster_id:
            if last_poster_id == request.user.id:
                last_posters[request.user.id] = request.user
            else:
                last_posters_ids.add(last_poster_id)

    if last_posters_ids:
        users_qs = (
            get_user_model()
            .objects.filter(id__in=last_posters_ids)
            .select_related("rank")
        )
        for user in users_qs:
            last_posters[user.id] = user

    return last_posters
