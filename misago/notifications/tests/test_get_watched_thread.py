from ..models import WatchedThread
from ..threads import get_watched_thread


def test_get_watched_thread_returns_null_if_thread_is_not_watched(user, old_thread):
    watched_thread = get_watched_thread(user, old_thread)
    assert watched_thread is None


def test_get_watched_thread_returns_watched_thread_for_user(
    watched_thread_factory, user, other_user, old_thread
):
    watched_thread_factory(other_user, old_thread, send_emails=True)
    user_watched_thread = watched_thread_factory(user, old_thread, send_emails=True)

    watched_thread = get_watched_thread(user, old_thread)
    assert watched_thread == user_watched_thread


def test_get_watched_thread_returns_null_for_user_if_thread_is_not_watched_but_other_thread_is(
    watched_thread_factory, user, old_thread, old_other_user_thread
):
    watched_thread_factory(user, old_other_user_thread, send_emails=True)

    watched_thread = get_watched_thread(user, old_thread)
    assert watched_thread is None


def test_get_watched_thread_returns_first_watched_thread_for_user_if_multiple_exist(
    watched_thread_factory, user, old_thread
):
    first_watched_thread = watched_thread_factory(user, old_thread, send_emails=True)
    watched_thread_factory(user, old_thread, send_emails=False)

    watched_thread = get_watched_thread(user, old_thread)
    assert watched_thread == first_watched_thread


def test_get_watched_thread_removes_extra_watched_threads_for_user(
    watched_thread_factory, user, old_thread
):
    first_watched_thread = watched_thread_factory(user, old_thread, send_emails=True)
    watched_thread_factory(user, old_thread, send_emails=False)

    assert WatchedThread.objects.count() == 2

    watched_thread = get_watched_thread(user, old_thread)
    assert watched_thread == first_watched_thread

    assert WatchedThread.objects.count() == 1
