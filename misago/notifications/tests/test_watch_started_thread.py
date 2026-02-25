from ..models import WatchedThread
from ..threads import ThreadNotifications, watch_started_thread


def test_watch_started_thread_creates_watched_thread_instance(user, thread):
    user.watch_started_threads = ThreadNotifications.SITE_AND_EMAIL
    user.save()

    watch_started_thread(thread, user)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.send_emails


def test_watch_started_thread_creates_watched_thread_instance_without_email_notifications(
    user, thread
):
    user.watch_started_threads = ThreadNotifications.SITE_ONLY
    user.save()

    watch_started_thread(thread, user)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert not watched_thread.send_emails


def test_watch_started_thread_doesnt_create_watched_thread_if_option_is_disabled(
    user, thread
):
    user.watch_started_threads = ThreadNotifications.NONE
    user.save()

    watch_started_thread(thread, user)

    assert not WatchedThread.objects.exists()
