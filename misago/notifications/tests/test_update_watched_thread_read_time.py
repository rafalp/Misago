from django.utils import timezone

from ..threads import update_watched_thread_read_time


def test_update_watched_thread_read_time_updates_watched_thread_read_time(
    thread, user, watched_thread_factory
):
    watched_thread = watched_thread_factory(user, thread, False)

    new_read_time = timezone.now()
    update_watched_thread_read_time(user, thread, new_read_time)

    watched_thread.refresh_from_db()
    assert watched_thread.read_time == new_read_time


def test_update_watched_thread_read_time_doesnt_update_other_threads_entries(
    thread, other_thread, user, watched_thread_factory
):
    watched_thread = watched_thread_factory(user, other_thread, False)

    new_read_time = timezone.now()
    update_watched_thread_read_time(user, thread, new_read_time)

    watched_thread.refresh_from_db()
    assert watched_thread.read_time != new_read_time


def test_update_watched_thread_read_time_doesnt_update_other_users_entries(
    thread, user, other_user, watched_thread_factory
):
    watched_thread = watched_thread_factory(other_user, thread, False)

    new_read_time = timezone.now()
    update_watched_thread_read_time(user, thread, new_read_time)

    watched_thread.refresh_from_db()
    assert watched_thread.read_time != new_read_time


def test_update_watched_thread_read_time_does_nothing_if_watched_thread_doesnt_exist(
    thread, user
):
    new_read_time = timezone.now()
    update_watched_thread_read_time(user, thread, new_read_time)
