from datetime import timedelta

from django.utils import timezone

from ..models import ReadThread
from ..tracker import mark_thread_read


def test_mark_thread_read_creates_read_thread_for_thread_without_user_readthread(
    user, default_category, thread
):
    read_time = timezone.now()

    mark_thread_read(user, thread, read_time)

    ReadThread.objects.get(
        user=user,
        category=default_category,
        thread=thread,
        read_time=read_time,
    )


def test_mark_thread_read_creates_read_thread_for_thread_with_empty_user_readthread(
    user, default_category, thread
):
    read_time = timezone.now()

    thread.user_readthread = None
    mark_thread_read(user, thread, read_time)

    ReadThread.objects.get(
        user=user,
        category=default_category,
        thread=thread,
        read_time=read_time,
    )


def test_mark_thread_read_updates_read_thread_for_thread_with_user_readthread(
    user, default_category, thread
):
    read_time = timezone.now()
    old_read_time = read_time - timedelta(hours=24 * 5)

    read_thread = ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=old_read_time,
    )

    thread.user_readthread = read_thread
    mark_thread_read(user, thread, read_time)

    read_thread.refresh_from_db()
    assert read_thread.read_time == read_time
