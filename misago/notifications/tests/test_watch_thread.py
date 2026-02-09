import pytest

from ..models import WatchedThread
from ..threads import watch_thread


def test_watch_thread_creates_watched_thread_instance(user, thread):
    watched_thread = watch_thread(thread, user)

    assert watched_thread.category == thread.category
    assert watched_thread.thread == thread
    assert watched_thread.user == user
    assert watched_thread.send_emails

    watched_thread.refresh_from_db()

    assert watched_thread.category == thread.category
    assert watched_thread.thread == thread
    assert watched_thread.user == user
    assert watched_thread.send_emails


def test_watch_thread_creates_watched_thread_instance_with_emails_disabled(
    user, thread
):
    watched_thread = watch_thread(thread, user, send_emails=False)

    assert watched_thread.category == thread.category
    assert watched_thread.thread == thread
    assert watched_thread.user == user
    assert not watched_thread.send_emails

    watched_thread.refresh_from_db()

    assert watched_thread.category == thread.category
    assert watched_thread.thread == thread
    assert watched_thread.user == user
    assert not watched_thread.send_emails


def test_watch_thread_with_commit_false_doesnt_save_watched_thread_instance_in_datatabase(
    django_assert_num_queries, user, thread
):
    with django_assert_num_queries(0):
        watched_thread = watch_thread(thread, user, commit=False)

    assert watched_thread.category == thread.category
    assert watched_thread.thread == thread
    assert watched_thread.user == user
    assert watched_thread.send_emails

    with pytest.raises(WatchedThread.DoesNotExist):
        watched_thread.refresh_from_db()


def test_watch_thread_creates_watched_thread_instance(user, thread):
    watched_thread = watch_thread(thread, user)

    assert watched_thread.category == thread.category
    assert watched_thread.thread == thread
    assert watched_thread.user == user
    assert watched_thread.send_emails

    watched_thread.refresh_from_db()

    assert watched_thread.category == thread.category
    assert watched_thread.thread == thread
    assert watched_thread.user == user
    assert watched_thread.send_emails
