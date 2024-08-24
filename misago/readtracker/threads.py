from datetime import datetime
from typing import Iterable

from django.http import HttpRequest
from django.db.models import OuterRef

from ..threads.models import Thread
from .cutoffdate import get_cutoff_date
from .models import ReadThread


def annotate_threads_read_time(user, queryset):
    if user.is_anonymous:
        return queryset

    return queryset.annotate(
        read_time=ReadThread.objects.filter(
            user=user,
            thread=OuterRef("id"),
        ).values("read_time"),
        category_read_time=ReadThread.objects.filter(
            user=user,
            category=OuterRef("category_id"),
        ).values("read_time"),
    )


def get_threads_new_posts(
    request: HttpRequest,
    threads: Iterable[Thread],
) -> dict[int, bool]:
    if not threads:
        return {}

    if request.user.is_anonymous:
        return {thread.id: False for thread in threads}

    cutoff = get_cutoff_date(request.settings, request.user)

    read_data = {}
    for thread in threads:
        read_data[thread.id] = get_thread_new_posts_status(thread, cutoff)

    return read_data


def get_thread_new_posts_status(
    thread: Thread,
    cutoff: datetime,
) -> bool:
    if not thread.last_post_on:
        return False

    if thread.last_post_on < cutoff:
        return False

    if thread.category_read_time and thread.last_post_on < thread.category_read_time:
        return False

    if not thread.read_time:
        return True

    return thread.last_post_on > thread.read_time
