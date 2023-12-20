from typing import Iterable

from django.http import HttpRequest

from ..categories.models import Category
from ..threads.models import Post, Thread
from ..threads.permissions import exclude_invisible_posts, exclude_invisible_threads
from .cutoffdate import get_cutoff_date


def get_categories_new_posts(
    request: HttpRequest,
    categories: Iterable[Category],
) -> dict[int, bool]:
    """Returns a dict with category ID as a key and bool if it has new posts."""
    if not categories:
        return {}

    categories_new_posts = {category.id: False for category in categories}

    if request.user.is_anonymous:
        return categories_new_posts

    threads = Thread.objects.filter(category__in=categories)
    threads = exclude_invisible_threads(request.user_acl, categories, threads)
    queryset = (
        Post.objects.filter(
            category__in=categories,
            thread__in=threads,
            posted_on__gt=get_cutoff_date(request.settings, request.user),
        )
        .values_list("category", flat=True)
        .distinct()
    )

    queryset = queryset.exclude(id__in=request.user.postread_set.values("post"))
    queryset = exclude_invisible_posts(request.user_acl, categories, queryset)

    for category_id in queryset:
        categories_new_posts[category_id] = True

    return categories_new_posts
