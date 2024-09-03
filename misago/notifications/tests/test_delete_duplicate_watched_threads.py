from datetime import timedelta

import pytest
from django.utils import timezone

from ..models import WatchedThread
from ..tasks import delete_duplicate_watched_threads


def test_delete_duplicate_watched_threads_deletes_duplicates_ordered_by_read_time_desc(
    user, thread
):
    kept_watched_thread = WatchedThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        read_time=timezone.now(),
    )
    deleted_watched_thread = WatchedThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        read_time=timezone.now() - timedelta(seconds=30),
    )

    delete_duplicate_watched_threads(thread.id)

    kept_watched_thread.refresh_from_db()

    with pytest.raises(WatchedThread.DoesNotExist):
        deleted_watched_thread.refresh_from_db()

    assert WatchedThread.objects.count() == 1


def test_delete_duplicate_watched_threads_keeps_email_notifications(user, thread):
    kept_watched_thread = WatchedThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        send_emails=False,
        read_time=timezone.now(),
    )
    deleted_watched_thread = WatchedThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        send_emails=True,
        read_time=timezone.now() - timedelta(seconds=30),
    )

    delete_duplicate_watched_threads(thread.id)

    kept_watched_thread.refresh_from_db()
    assert kept_watched_thread.send_emails

    with pytest.raises(WatchedThread.DoesNotExist):
        deleted_watched_thread.refresh_from_db()

    assert WatchedThread.objects.count() == 1


def test_delete_duplicate_watched_threads_skips_non_duplicated_watched_threads(
    user, other_user, thread
):
    kept_watched_thread = WatchedThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        read_time=timezone.now(),
    )
    deleted_watched_thread = WatchedThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        read_time=timezone.now() - timedelta(seconds=30),
    )

    other_kept_watched_thread = WatchedThread.objects.create(
        user=other_user,
        category=thread.category,
        thread=thread,
        read_time=timezone.now(),
    )

    delete_duplicate_watched_threads(thread.id)

    kept_watched_thread.refresh_from_db()
    other_kept_watched_thread.refresh_from_db()

    with pytest.raises(WatchedThread.DoesNotExist):
        deleted_watched_thread.refresh_from_db()

    assert WatchedThread.objects.count() == 2


def test_delete_duplicate_watched_threads_skips_other_threads_watched_threads(
    user, other_user, thread, other_thread
):
    kept_watched_thread = WatchedThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        read_time=timezone.now(),
    )
    deleted_watched_thread = WatchedThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        read_time=timezone.now() - timedelta(seconds=30),
    )

    other_kept_watched_thread = WatchedThread.objects.create(
        user=other_user,
        category=thread.category,
        thread=thread,
        read_time=timezone.now(),
    )

    other_thread_watched_thread = WatchedThread.objects.create(
        user=other_user,
        category=other_thread.category,
        thread=other_thread,
        read_time=timezone.now(),
    )
    other_thread_watched_thread_duplicate = WatchedThread.objects.create(
        user=other_user,
        category=other_thread.category,
        thread=other_thread,
        read_time=timezone.now(),
    )

    delete_duplicate_watched_threads(thread.id)

    other_thread_watched_thread.refresh_from_db()
    other_thread_watched_thread_duplicate.refresh_from_db()

    kept_watched_thread.refresh_from_db()
    other_kept_watched_thread.refresh_from_db()

    with pytest.raises(WatchedThread.DoesNotExist):
        deleted_watched_thread.refresh_from_db()

    assert WatchedThread.objects.count() == 4
