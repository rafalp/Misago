from datetime import datetime
from typing import TYPE_CHECKING, Iterable

from django.http import HttpRequest
from django.db.models import FilteredRelation, OuterRef, Q

from ..categories.models import Category
from ..threads.models import Post, Thread
from .readtime import get_default_read_time
from .models import ReadCategory, ReadThread

if TYPE_CHECKING:
    from ..users.models import User


def categories_select_related_user_readcategory(queryset, user):
    if user.is_anonymous:
        return queryset

    return queryset.select_related("user_readcategory").annotate(
        user_readcategory=FilteredRelation(
            "readcategory",
            condition=Q(readcategory__user=user),
        )
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


def get_category_read_time(category: Category) -> datetime | None:
    if user_readcategory := getattr(category, "user_readcategory", None):
        return user_readcategory.read_time

    return None


def is_category_unread(
    category: Category,
    default_read_time: datetime,
) -> bool:
    if not category.last_posted_at:
        return False

    if category.last_posted_at < default_read_time:
        return False

    if user_readcategory := getattr(category, "user_readcategory", None):
        return category.last_posted_at > user_readcategory.read_time

    return True


def threads_annotate_user_readcategory_time(queryset, user):
    if user.is_anonymous:
        return queryset

    return queryset.annotate(
        user_readcategory_time=ReadCategory.objects.filter(
            user=user,
            category=OuterRef("category_id"),
        ).values("read_time"),
    )


def threads_select_related_user_readthread(queryset, user):
    if user.is_anonymous:
        return queryset

    return queryset.select_related("user_readthread").annotate(
        user_readthread=FilteredRelation(
            "readthread",
            condition=Q(readthread__user=user),
        ),
    )


def get_unread_threads(request: HttpRequest, threads: Iterable[Thread]) -> set[int]:
    if not threads or request.user.is_anonymous:
        return set()

    default_read_time = get_default_read_time(request.settings, request.user)

    unreadthreads: set[int] = set()
    for thread in threads:
        if is_thread_unread(thread, default_read_time):
            unreadthreads.add(thread.id)

    return unreadthreads


def is_thread_unread(
    thread: Thread,
    default_read_time: datetime,
) -> bool:
    if not thread.last_posted_at:
        return False

    if thread.last_posted_at < default_read_time:
        return False

    if (
        thread.user_readcategory_time
        and thread.last_posted_at <= thread.user_readcategory_time
    ):
        return False

    if user_readthread := getattr(thread, "user_readthread", None):
        return thread.last_posted_at > user_readthread.read_time

    return True


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
        if post.posted_at > read_time:
            read_data.add(post.id)

    return read_data


def get_thread_read_time(request: HttpRequest, thread: Thread) -> datetime:
    default_read_time = get_default_read_time(request.settings, request.user)
    category_read_time = thread.user_readcategory_time
    thread_read_time = None

    if user_readthread := getattr(thread, "user_readthread", None):
        thread_read_time = user_readthread.read_time

    if thread_read_time and category_read_time:
        read_time = max(thread_read_time, category_read_time)
    elif thread_read_time:
        read_time = thread_read_time
    elif category_read_time:
        read_time = category_read_time
    else:
        return default_read_time

    return max(read_time, default_read_time)


def mark_thread_read(user: "User", thread: Thread, read_time: datetime):
    create_row = True

    if getattr(thread, "user_readthread", None):
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
    if not category.last_posted_at:
        raise ValueError("'Category.last_posted_at' can't be 'None'")

    create_row = True

    if force_update or getattr(category, "user_readcategory", None):
        create_row = not ReadCategory.objects.filter(
            user=user,
            category=category,
        ).update(read_time=category.last_posted_at)

    if create_row:
        ReadCategory.objects.create(
            user=user,
            category=category,
            read_time=category.last_posted_at,
        )

    ReadThread.objects.filter(user=user, category=category).delete()
