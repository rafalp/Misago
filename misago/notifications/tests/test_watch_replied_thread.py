from ..models import WatchedThread
from ..threads import ThreadNotifications, watch_replied_thread


def test_replied_thread_is_watched_with_email_notifications(user, thread):
    user.watch_replied_threads = ThreadNotifications.SITE_AND_EMAIL
    user.save()

    watch_replied_thread(user, thread)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.send_emails


def test_replied_thread_is_watched_without_email_notifications(user, thread):
    user.watch_replied_threads = ThreadNotifications.SITE_ONLY
    user.save()

    watch_replied_thread(user, thread)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert not watched_thread.send_emails


def test_replied_thread_is_not_watched_if_option_is_disabled(user, thread):
    user.watch_replied_threads = ThreadNotifications.NONE
    user.save()

    watch_replied_thread(user, thread)

    assert not WatchedThread.objects.exists()


def test_replied_thread_watching_entry_notification_emails_are_not_disabled(
    user, thread, watched_thread_factory
):
    user.watch_replied_threads = ThreadNotifications.SITE_ONLY
    user.save()

    watched_thread = watched_thread_factory(user, thread, send_emails=True)

    watch_replied_thread(user, thread)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.send_emails


def test_replied_thread_watching_entry_notification_emails_are_not_enabled(
    user, thread, watched_thread_factory
):
    user.watch_replied_threads = ThreadNotifications.SITE_AND_EMAIL
    user.save()

    watched_thread = watched_thread_factory(user, thread, send_emails=False)

    watch_replied_thread(user, thread)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert not watched_thread.send_emails


def test_replied_thread_watching_entry_is_not_removed_if_option_is_disabled(
    user, thread, watched_thread_factory
):
    user.watch_replied_threads = ThreadNotifications.NONE
    user.save()

    watched_thread = watched_thread_factory(user, thread, send_emails=False)

    watch_replied_thread(user, thread)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert not watched_thread.send_emails
