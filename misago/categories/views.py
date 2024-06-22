from typing import TYPE_CHECKING, Union

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from ..permissions.enums import CategoryPermission
from ..permissions.proxy import UserPermissionsProxy
from ..readtracker.categories import get_categories_new_posts
from ..users.models import User
from .enums import CategoryTree
from .models import Category

if TYPE_CHECKING:
    from ..users.models import User


def index(request, *args, is_index: bool | None = None, **kwargs):
    if not is_index and request.settings.index_view == "categories":
        return redirect(reverse("misago:index"))

    categories_list = get_categories_list(request)

    return render(
        request,
        "misago/categories/index.html",
        {
            "is_index": is_index,
            "categories_list": categories_list,
        },
    )


def get_categories_list(request: HttpRequest):
    if not request.user_permissions.categories[CategoryPermission.SEE]:
        return []

    categories_data = get_categories_data(request.user_permissions)
    last_posters = prefetch_last_posters(request, categories_data.values())
    new_posts: dict[int, bool] = {}

    if request.user.is_authenticated:
        new_posts = get_categories_new_posts(
            request,
            [item["category"] for item in categories_data.values()],
        )

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

        # Set read state
        if request.user.is_authenticated and new_posts[category.id]:
            category_data["new_posts"] = True
            category_data["children_new_posts"] = True

        # Aggregate data from category to its parent
        if category.level > 1:
            parent = categories_data[category.parent_id]
            aggregate_category_to_its_parent(category_data, parent)

    # Return root categories
    return [
        category for category in categories_data.values() if show_top_category(category)
    ]


def get_categories_data(permissions: UserPermissionsProxy) -> dict:
    categories_qs = Category.objects.filter(
        id__in=permissions.categories[CategoryPermission.SEE],
        tree_id=CategoryTree.THREADS,
        level__gt=0,
    )

    categories_data: dict[int, dict] = {}

    for category in categories_qs:
        categories_data[category.id] = get_category_data(category, permissions)

    return categories_data


def get_category_data(category: Category, permissions: UserPermissionsProxy) -> dict:
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
        "new_posts": False,
        "can_browse": (
            category.id in permissions.categories[CategoryPermission.BROWSE]
            or category.delay_browse_check
        ),
        "show_started_only": category.show_started_only,
        "children": [],
        "children_threads": category.threads,
        "children_posts": category.posts,
        "children_last_thread": category_last_thread,
        "children_new_posts": False,
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
        and category.id not in permissions.categories_moderator
        and (user.is_anonymous or category.last_poster_id != user.id)
    ):
        return False

    return True


def prefetch_last_posters(
    request: HttpRequest, categories_list: list[dict]
) -> dict[int, User]:
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
        users_qs = User.objects.filter(id__in=last_posters_ids).select_related("rank")
        for user in users_qs:
            last_posters[user.id] = user

    return last_posters


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
    if category["children_new_posts"]:
        parent["children_new_posts"] = True

    parent["children"].insert(0, category)


def show_top_category(category: dict) -> bool:
    if category["category"].level != 1:
        return False

    if category["category"].is_vanilla and not category["children"]:
        return False

    return True
