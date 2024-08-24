from datetime import datetime
from typing import Iterable

from django.http import HttpRequest
from django.db.models import OuterRef

from ..categories.models import Category
from .cutoffdate import get_cutoff_date
from .models import ReadCategory


def annotate_categories_read_time(user, queryset):
    if user.is_anonymous:
        return queryset

    return queryset.annotate(
        read_time=ReadCategory.objects.filter(
            user=user,
            category=OuterRef("id"),
        ).values("read_time"),
    )


def get_categories_new_posts(
    request: HttpRequest,
    categories: Iterable[Category],
) -> dict[int, bool]:
    if not categories:
        return {}

    if request.user.is_anonymous:
        return {category.id: False for category in categories}

    cutoff = get_cutoff_date(request.settings, request.user)

    read_data = {}
    for category in categories:
        read_data[category.id] = get_category_new_posts_status(category, cutoff)

    return read_data


def get_category_new_posts_status(
    category: Category,
    cutoff: datetime,
) -> bool:
    if not category.last_post_on:
        return False

    if category.last_post_on < cutoff:
        return False

    if not category.read_time:
        return True

    return category.last_post_on > category.read_time
