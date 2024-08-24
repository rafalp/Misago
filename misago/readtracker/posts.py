from datetime import datetime
from typing import Iterable

from django.http import HttpRequest

from ..threads.models import Post, Thread
from .cutoffdate import get_cutoff_date


def get_thread_posts_new_status(
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
    cutoff_time = get_cutoff_date(request.settings, request.user)

    if thread.read_time and thread.category_read_time:
        read_time = max(thread.read_time, thread.category_read_time)
    elif thread.read_time:
        read_time = thread.read_time
    elif thread.category_read_time:
        read_time = thread.category_read_time
    else:
        read_time = cutoff_time

    return max(read_time, cutoff_time)
