from django.utils import timezone

from ..threads import update_watched_thread_read_time


def test_update_watched_thread_read_time_updates_watched_thread_read_time(
    watched_thread_factory, user, old_thread
):
    watched_thread = watched_thread_factory(user, old_thread, False)

    new_read_time = timezone.now()
    update_watched_thread_read_time(user, old_thread, new_read_time)

    watched_thread.refresh_from_db()
    assert watched_thread.read_time == new_read_time


def test_update_watched_thread_read_time_doesnt_update_other_threads_entries(
    watched_thread_factory, user, old_thread, old_other_user_thread
):
    watched_thread = watched_thread_factory(user, old_other_user_thread, False)

    new_read_time = timezone.now()
    update_watched_thread_read_time(user, old_thread, new_read_time)

    watched_thread.refresh_from_db()
    assert watched_thread.read_time != new_read_time


def test_update_watched_thread_read_time_doesnt_update_other_users_entries(
    watched_thread_factory, user, other_user, old_thread
):
    watched_thread = watched_thread_factory(other_user, old_thread, False)

    new_read_time = timezone.now()
    update_watched_thread_read_time(user, old_thread, new_read_time)

    watched_thread.refresh_from_db()
    assert watched_thread.read_time != new_read_time


def test_update_watched_thread_read_time_does_nothing_if_watched_thread_doesnt_exist(
    user, old_thread
):
    new_read_time = timezone.now()
    update_watched_thread_read_time(user, old_thread, new_read_time)
