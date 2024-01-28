from django.http import HttpRequest
from django.shortcuts import render

from ..readtracker.categories import get_categories_new_posts
from ..users.models import User
from .enums import CategoryTree
from .models import Category


def index(request):
    categories_list = get_categories_list(request)

    return render(
        request,
        "misago/categories/index.html",
        {"categories_list": categories_list},
    )


def get_categories_list(request: HttpRequest):
    if not request.user_acl["visible_categories"]:
        return []

    categories_qs = Category.objects.filter(
        id__in=request.user_acl["visible_categories"],
        tree_id=CategoryTree.THREADS,
        level__gt=0,
    )

    categories_map: dict[int, dict] = {}

    for category in categories_qs:
        category_permissions = request.user_acl["categories"][category.id]

        if category.last_thread_id:
            category_last_thread = {
                "id": category.last_thread_id,
                "title": category.last_thread_title,
                "slug": category.last_thread_slug,
                "last_post_on": category.last_post_on,
                "last_poster": None,
                "last_poster_name": category.last_poster_name,
            }
        else:
            category_last_thread = None

        categories_map[category.id] = {
            "category": category,
            "threads": category.threads,
            "posts": category.posts,
            "last_thread": category_last_thread,
            "new_posts": False,
            "is_protected": category.id
            not in request.user_acl["browseable_categories"],
            "is_private": not category_permissions["can_see_all_threads"],
            "children": [],
            "children_threads": category.threads,
            "children_posts": category.posts,
            "children_last_thread": category_last_thread,
            "children_new_posts": False,
        }

    last_posters = prefetch_last_posters(request, categories_map.values())
    new_posts: dict[int, bool] = {}

    if request.user.is_authenticated:
        new_posts = get_categories_new_posts(
            request,
            [item["category"] for item in categories_map.values()],
        )

    # Populate categories last posters and read states
    # Aggregate categories to their parents
    for item in reversed(categories_map.values()):
        category = item["category"]

        if category.last_poster_id:
            last_poster = last_posters[category.last_poster_id]
            item["last_thread"].update(
                {
                    "last_poster": last_poster,
                    "last_poster_name": last_poster.username,
                }
            )

        if request.user.is_authenticated and new_posts[category.id]:
            item["new_posts"] = True
            item["children_new_posts"] = True

        if category.level > 1:
            parent = categories_map[category.parent_id]

            # Add item's aggregated stats to parent's
            parent["children_threads"] += item["children_threads"]
            parent["children_posts"] += item["children_posts"]

            # Update parent's last thread if they don't have one or its older
            item_last_thread = item["children_last_thread"]
            parent_last_thread = parent["children_last_thread"]
            if item_last_thread and (
                not parent_last_thread
                or item_last_thread["last_post_on"] > parent_last_thread["last_post_on"]
            ):
                parent["children_last_thread"] = item_last_thread

            # Propagate to parent the new posts status
            if item["children_new_posts"]:
                parent["children_new_posts"] = True

            parent["children"].insert(0, item)

    return [
        category
        for category in categories_map.values()
        if category["category"].level == 1
    ]


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
