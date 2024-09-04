from datetime import datetime
from typing import TYPE_CHECKING, Iterable

from django.http import HttpRequest
from django.db.models import OuterRef

from ..categories.models import Category
from ..threads.models import Post, Thread
from .readtime import get_default_read_time
from .models import ReadCategory, ReadThread

if TYPE_CHECKING:
    from ..users.models import User


def annotate_categories_read_time(user, queryset):
    if user.is_anonymous:
        return queryset

    return queryset.annotate(
        read_time=ReadCategory.objects.filter(
            user=user,
            category=OuterRef("id"),
        ).values("read_time"),
    )


def get_unread_categories(
    request: HttpRequest, categories: Iterable[Category]
) -> set[int]:
    if not categories or request.user.is_anonymous:
        return set()

    default_read_time = get_default_read_time(request.settings, request.user)

    unread_categories: set[int] = set()
    for category in categories:
        if is_category_unread(category, default_read_time):
            unread_categories.add(category.id)

    return unread_categories


def is_category_unread(
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


def annotate_threads_read_time(user, queryset, *, with_category: bool = True):
    if user.is_anonymous:
        return queryset

    queryset = queryset.annotate(
        read_time=ReadThread.objects.filter(
            user=user,
            thread=OuterRef("id"),
        ).values("read_time"),
    )

    if with_category:
        queryset = queryset.annotate(
            category_read_time=ReadCategory.objects.filter(
                user=user,
                category=OuterRef("category_id"),
            ).values("read_time"),
        )

    return queryset


def get_unread_threads(request: HttpRequest, threads: Iterable[Thread]) -> set[int]:
    if not threads or request.user.is_anonymous:
        return set()

    default_read_time = get_default_read_time(request.settings, request.user)

    unread_threads: set[int] = set()
    for thread in threads:
        if is_thread_unread(thread, default_read_time):
            unread_threads.add(thread.id)

    return unread_threads


def is_thread_unread(
    thread: Thread,
    default_read_time: datetime,
) -> bool:
    if not thread.last_post_on:
        return False

    if thread.last_post_on < default_read_time:
        return False

    if thread.category_read_time and thread.last_post_on <= thread.category_read_time:
        return False

    if not thread.read_time:
        return True

    return thread.last_post_on > thread.read_time


def get_unread_posts(
    request: HttpRequest,
    thread: Thread,
    posts: Iterable[Post],
) -> set[int]:
    if not posts or request.user.is_anonymous:
        return set()

    read_time = get_thread_read_time(request, thread)

    read_data: set[int] = set()
    for post in posts:
        if post.posted_on > read_time:
            read_data.add(post.id)

    return read_data


def get_thread_read_time(request: HttpRequest, thread: Thread) -> datetime:
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


def mark_thread_read(user: "User", thread: Thread, read_time: datetime):
    create_row = True

    if getattr(thread, "read_time", None):
        create_row = not ReadThread.objects.filter(
            user=user,
            thread=thread,
        ).update(read_time=read_time)

    if create_row:
        ReadThread.objects.create(
            user=user,
            thread=thread,
            category=thread.category,
            read_time=read_time,
        )


def mark_category_read(user: "User", category: Category, *, force_update: bool = False):
    create_row = True

    if force_update or getattr(category, "read_time", None):
        create_row = not ReadCategory.objects.filter(
            user=user,
            category=category,
        ).update(read_time=category.last_post_on)

    if create_row:
        ReadCategory.objects.create(
            user=user,
            category=category,
            read_time=category.last_post_on,
        )

    ReadThread.objects.filter(user=user, category=category).delete()
