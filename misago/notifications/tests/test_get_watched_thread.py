from ..enums import ThreadNotifications
from ..models import WatchedThread
from ..threads import get_watched_thread


def test_get_watched_thread_returns_null_if_thread_is_not_watched(user, thread):
    watched_thread = get_watched_thread(user, thread)
    assert watched_thread is None


def test_get_watched_thread_returns_watched_thread_for_user(
    user, other_user, thread, watched_thread_factory
):
    watched_thread_factory(other_user, thread, ThreadNotifications.NONE)
    user_watched_thread = watched_thread_factory(user, thread, ThreadNotifications.NONE)

    watched_thread = get_watched_thread(user, thread)
    assert watched_thread == user_watched_thread


def test_get_watched_thread_returns_watched_thread_for_user_and_thread(
    user, thread, other_thread, watched_thread_factory
):
    watched_thread_factory(user, other_thread)

    watched_thread = get_watched_thread(user, thread)
    assert watched_thread is None


def test_get_watched_thread_returns_first_watched_thread_for_user_if_multiple_exist(
    user, thread, watched_thread_factory
):
    first_watched_thread = watched_thread_factory(
        user, thread, ThreadNotifications.NONE
    )
    watched_thread_factory(user, thread, ThreadNotifications.NONE)

    watched_thread = get_watched_thread(user, thread)
    assert watched_thread == first_watched_thread


def test_get_watched_thread_removes_extra_watched_threads_for_user(
    user, thread, watched_thread_factory
):
    first_watched_thread = watched_thread_factory(
        user, thread, ThreadNotifications.NONE
    )
    watched_thread_factory(user, thread, ThreadNotifications.NONE)

    assert WatchedThread.objects.count() == 2

    watched_thread = get_watched_thread(user, thread)
    assert watched_thread == first_watched_thread

    assert WatchedThread.objects.count() == 1
