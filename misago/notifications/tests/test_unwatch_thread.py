import pytest

from ..models import WatchedThread
from ..threads import unwatch_thread, watch_thread


def test_unwatch_thread_deletes_watched_thread_entry_for_user_and_thread(user, thread):
    watched_thread = watch_thread(thread, user)

    assert unwatch_thread(thread, user)

    with pytest.raises(WatchedThread.DoesNotExist):
        watched_thread.refresh_from_db()


def test_unwatch_thread_deletes_multiple_watched_thread_entries_for_user_and_thread(
    user, thread
):
    watched_thread = watch_thread(thread, user)
    watched_thread_other = watch_thread(thread, user)

    assert unwatch_thread(thread, user)

    with pytest.raises(WatchedThread.DoesNotExist):
        watched_thread.refresh_from_db()

    with pytest.raises(WatchedThread.DoesNotExist):
        watched_thread_other.refresh_from_db()


def test_unwatch_thread_doesnt_delete_other_users_watched_thread_entries(
    user, other_user, thread
):
    watched_thread = watch_thread(thread, user)
    other_user_watched_thread = watch_thread(thread, other_user)

    assert unwatch_thread(thread, user)

    with pytest.raises(WatchedThread.DoesNotExist):
        watched_thread.refresh_from_db()

    other_user_watched_thread.refresh_from_db()


def test_unwatch_thread_doesnt_delete_other_threads_watched_thread_entries(
    user, thread, user_thread
):
    watched_thread = watch_thread(thread, user)
    other_thread_watched_thread = watch_thread(user_thread, user)

    assert unwatch_thread(thread, user)

    with pytest.raises(WatchedThread.DoesNotExist):
        watched_thread.refresh_from_db()

    other_thread_watched_thread.refresh_from_db()


def test_unwatch_thread_returns_false_if_user_is_not_watching_thread(user, thread):
    assert not unwatch_thread(thread, user)
