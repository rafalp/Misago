import pytest

from ..models import WatchedThread
from ..threads import ThreadNotifications, watch_replied_thread


def test_watch_replied_thread_creates_watched_thread(user, old_thread):
    user.watch_replied_threads = ThreadNotifications.SITE_AND_EMAIL
    user.save()

    watch_replied_thread(old_thread, user)

    watched_thread = WatchedThread.objects.get(user=user, thread=old_thread)
    assert watched_thread.send_emails


def test_watch_replied_thread_creates_watched_thread_without_email_notifications(
    user, old_thread
):
    user.watch_replied_threads = ThreadNotifications.SITE_ONLY
    user.save()

    watch_replied_thread(old_thread, user)

    watched_thread = WatchedThread.objects.get(user=user, thread=old_thread)
    assert not watched_thread.send_emails


def test_watch_replied_thread_doesnt_create_watched_thread_if_option_is_disabled(
    user, old_thread
):
    user.watch_replied_threads = ThreadNotifications.NONE
    user.save()

    watch_replied_thread(old_thread, user)

    assert not WatchedThread.objects.exists()


def test_watch_replied_thread_replaces_watched_thread_with_new_instance(
    watched_thread_factory, user, old_thread
):
    user.watch_replied_threads = ThreadNotifications.SITE_AND_EMAIL
    user.save()

    old_watched_thread = watched_thread_factory(user, old_thread, send_emails=False)

    watch_replied_thread(old_thread, user)

    watched_thread = WatchedThread.objects.get(user=user, thread=old_thread)
    assert watched_thread.send_emails

    with pytest.raises(WatchedThread.DoesNotExist):
        old_watched_thread.refresh_from_db()


def test_watch_replied_thread_doesnt_delete_existing_watched_thread_if_option_is_disabled(
    watched_thread_factory, user, old_thread
):
    user.watch_replied_threads = ThreadNotifications.NONE
    user.save()

    watched_thread = watched_thread_factory(user, old_thread, send_emails=False)

    watch_replied_thread(old_thread, user)

    watched_thread = WatchedThread.objects.get(user=user, thread=old_thread)
    assert not watched_thread.send_emails


def test_watch_replied_thread_with_commit_false_doesnt_save_watched_thread_instance_in_database(
    django_assert_num_queries, user, thread
):
    user.watch_replied_threads = ThreadNotifications.SITE_AND_EMAIL
    user.save()

    with django_assert_num_queries(1):
        watch_replied_thread(thread, user, commit=False)

    with pytest.raises(WatchedThread.DoesNotExist):
        WatchedThread.objects.get(user=user, thread=thread)
