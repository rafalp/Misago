from ..threads import ThreadNotifications, get_watched_threads


def test_get_watched_threads_returns_empty_dict_if_threads_are_not_watched(
    user, old_thread, old_other_user_thread
):
    watched_threads = get_watched_threads(user, [old_thread, old_other_user_thread])
    assert watched_threads == {}


def test_get_watched_threads_returns_watched_threads_for_user(
    watched_thread_factory, user, other_user, old_thread, old_other_user_thread
):
    watched_thread_factory(other_user, old_thread, send_emails=True)
    watched_thread_factory(user, old_thread, send_emails=False)
    watched_thread_factory(user, old_other_user_thread, send_emails=True)

    watched_threads = get_watched_threads(user, [old_thread, old_other_user_thread])
    assert watched_threads == {
        old_thread.id: ThreadNotifications.SITE_ONLY,
        old_other_user_thread.id: ThreadNotifications.SITE_AND_EMAIL,
    }


def test_get_watched_threads_excludes_unspecified_threads(
    watched_thread_factory, user, old_thread, old_other_user_thread
):
    watched_thread_factory(user, old_other_user_thread, send_emails=True)

    watched_threads = get_watched_threads(user, [old_thread])
    assert watched_threads == {}


def test_get_watched_threads_returns_first_watched_thread_for_user(
    watched_thread_factory, user, old_thread
):
    watched_thread_factory(user, old_thread, send_emails=False)
    watched_thread_factory(user, old_thread, send_emails=True)

    watched_threads = get_watched_threads(user, [old_thread])
    assert watched_threads == {old_thread.id: ThreadNotifications.SITE_ONLY}
