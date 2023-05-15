from ..threads import ThreadNotifications, get_watched_threads


def test_get_watched_threads_returns_empty_dict_if_threads_are_not_watched(
    user, thread, other_thread
):
    watched_threads = get_watched_threads(user, [thread, other_thread])
    assert watched_threads == {}


def test_get_watched_threads_returns_watched_threads_for_user(
    user, other_user, thread, other_thread, watched_thread_factory
):
    watched_thread_factory(other_user, thread, send_emails=True)
    watched_thread_factory(user, thread, send_emails=False)
    watched_thread_factory(user, other_thread, send_emails=True)

    watched_threads = get_watched_threads(user, [thread, other_thread])
    assert watched_threads == {
        thread.id: ThreadNotifications.SITE_ONLY,
        other_thread.id: ThreadNotifications.SITE_AND_EMAIL,
    }


def test_get_watched_threads_excludes_unspecified_threads(
    user, thread, other_thread, watched_thread_factory
):
    watched_thread_factory(user, other_thread, send_emails=True)

    watched_threads = get_watched_threads(user, [thread])
    assert watched_threads == {}


def test_get_watched_threads_returns_first_watched_thread_for_user(
    user, thread, watched_thread_factory
):
    watched_thread_factory(user, thread, send_emails=False)
    watched_thread_factory(user, thread, send_emails=True)

    watched_threads = get_watched_threads(user, [thread])
    assert watched_threads == {thread.id: ThreadNotifications.SITE_ONLY}
