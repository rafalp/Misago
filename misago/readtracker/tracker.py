from datetime import datetime
from typing import Iterable

from django.http import HttpRequest
from django.db.models import OuterRef

from ..categories.models import Category
from ..threads.models import Post, Thread
from .readtime import get_default_read_time
from .models import ReadCategory, ReadThread


def annotate_categories_read_time(user, queryset):
    if user.is_anonymous:
        return queryset

    return queryset.annotate(
        read_time=ReadCategory.objects.filter(
            user=user,
            category=OuterRef("id"),
        ).values("read_time"),
    )


def get_categories_unread_posts(
    request: HttpRequest,
    categories: Iterable[Category],
) -> dict[int, bool]:
    if not categories:
        return {}

    if request.user.is_anonymous:
        return {category.id: False for category in categories}

    default_read_time = get_default_read_time(request.settings, request.user)

    read_data = {}
    for category in categories:
        read_data[category.id] = get_category_unread_status(category, default_read_time)

    return read_data


def get_category_unread_status(
    category: Category,
    default_read_time: datetime,
) -> bool:
    if not category.last_post_on:
        return False

    if category.last_post_on < default_read_time:
        return False

    if not category.read_time:
        return True

    return category.last_post_on > category.read_time


def annotate_threads_read_time(user, queryset):
    if user.is_anonymous:
        return queryset

    return queryset.annotate(
        read_time=ReadThread.objects.filter(
            user=user,
            thread=OuterRef("id"),
        ).values("read_time"),
        category_read_time=ReadCategory.objects.filter(
            user=user,
            category=OuterRef("category_id"),
        ).values("read_time"),
    )


def get_threads_unread_posts(
    request: HttpRequest,
    threads: Iterable[Thread],
) -> dict[int, bool]:
    if not threads:
        return {}

    if request.user.is_anonymous:
        return {thread.id: False for thread in threads}

    default_read_time = get_default_read_time(request.settings, request.user)

    read_data = {}
    for thread in threads:
        read_data[thread.id] = get_thread_unread_status(thread, default_read_time)

    return read_data


def get_thread_unread_status(
    thread: Thread,
    default_read_time: datetime,
) -> bool:
    if not thread.last_post_on:
        return False

    if thread.last_post_on < default_read_time:
        return False

    if thread.category_read_time and thread.last_post_on < thread.category_read_time:
        return False

    if not thread.read_time:
        return True

    return thread.last_post_on > thread.read_time


def get_thread_posts_unread_status(
    request: HttpRequest,
    thread: Thread,
    posts: Iterable[Post],
) -> dict[int, bool]:
    if not posts:
        return {}

    if request.user.is_anonymous:
        return {post.id: False for post in posts}

    read_time = get_thread_posts_read_time(request, thread)

    read_data = {}
    for post in posts:
        read_data[post.id] = post.posted_on > read_time

    return read_data


def get_thread_posts_read_time(request: HttpRequest, thread: Thread) -> datetime:
    default_read_time = get_default_read_time(request.settings, request.user)

    if thread.read_time and thread.category_read_time:
        read_time = max(thread.read_time, thread.category_read_time)
    elif thread.read_time:
        read_time = thread.read_time
    elif thread.category_read_time:
        read_time = thread.category_read_time
    else:
        read_time = default_read_time

    return max(read_time, default_read_time)
