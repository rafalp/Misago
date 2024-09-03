from datetime import timedelta

from django.utils import timezone

from ..models import ReadThread
from ..tracker import mark_thread_read


def test_mark_thread_read_creates_read_thread_for_thread_without_read_time(
    user, default_category, thread
):
    read_time = timezone.now()

    thread.read_time = None
    mark_thread_read(user, thread, read_time)

    ReadThread.objects.get(
        user=user,
        category=default_category,
        thread=thread,
        read_time=read_time,
    )


def test_mark_thread_read_updates_read_thread_for_thread_with_read_time(
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

    thread.read_time = old_read_time
    mark_thread_read(user, thread, read_time)

    read_thread.refresh_from_db()
    assert read_thread.read_time == read_time


def test_mark_thread_read_creates_missing_read_thread_for_thread_with_read_time(
    user, default_category, thread
):
    read_time = timezone.now()
    old_read_time = read_time - timedelta(hours=24 * 5)

    thread.read_time = old_read_time
    mark_thread_read(user, thread, read_time)

    ReadThread.objects.get(
        user=user,
        category=default_category,
        thread=thread,
        read_time=read_time,
    )
