from ..models import WatchedThread
from ..threads import ThreadNotifications, watch_started_thread


def test_started_thread_is_watched_with_email_notifications(user, thread):
    user.watch_started_threads = ThreadNotifications.SITE_AND_EMAIL
    user.save()

    watch_started_thread(user, thread)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.send_emails


def test_started_thread_is_watched_without_email_notifications(user, thread):
    user.watch_started_threads = ThreadNotifications.SITE_ONLY
    user.save()

    watch_started_thread(user, thread)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert not watched_thread.send_emails


def test_started_thread_is_not_watched_if_option_is_disabled(user, thread):
    user.watch_started_threads = ThreadNotifications.NONE
    user.save()

    watch_started_thread(user, thread)

    assert not WatchedThread.objects.exists()
