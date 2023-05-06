from ..enums import ThreadNotifications
from ..models import WatchedThread
from ..threads import watch_replied_thread


def test_replied_thread_is_watched_with_email_notifications(user, thread):
    user.watch_replied_threads = ThreadNotifications.SEND_EMAIL
    user.save()

    watch_replied_thread(user, thread)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.notifications == ThreadNotifications.SEND_EMAIL


def test_replied_thread_is_watched_without_email_notifications(user, thread):
    user.watch_replied_threads = ThreadNotifications.DONT_EMAIL
    user.save()

    watch_replied_thread(user, thread)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.notifications == ThreadNotifications.DONT_EMAIL


def test_replied_thread_is_not_watched_if_option_is_disabled(user, thread):
    user.watch_replied_threads = ThreadNotifications.NONE
    user.save()

    watch_replied_thread(user, thread)

    assert not WatchedThread.objects.exists()


def test_replied_thread_watching_entry_is_reenabled_with_email_notifications(
    user, thread, watched_thread_factory
):
    user.watch_replied_threads = ThreadNotifications.SEND_EMAIL
    user.save()

    watched_thread = watched_thread_factory(user, thread, ThreadNotifications.NONE)

    watch_replied_thread(user, thread)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.notifications == ThreadNotifications.SEND_EMAIL


def test_replied_thread_watching_entry_is_reenabled_without_email_notifications(
    user, thread, watched_thread_factory
):
    user.watch_replied_threads = ThreadNotifications.DONT_EMAIL
    user.save()

    watched_thread = watched_thread_factory(user, thread, ThreadNotifications.NONE)

    watch_replied_thread(user, thread)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.notifications == ThreadNotifications.DONT_EMAIL


def test_replied_thread_watching_entry_notification_emails_are_not_disabled(
    user, thread, watched_thread_factory
):
    user.watch_replied_threads = ThreadNotifications.DONT_EMAIL
    user.save()

    watched_thread = watched_thread_factory(
        user, thread, ThreadNotifications.SEND_EMAIL
    )

    watch_replied_thread(user, thread)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.notifications == ThreadNotifications.SEND_EMAIL


def test_replied_thread_watching_entry_notification_emails_are_not_enabled(
    user, thread, watched_thread_factory
):
    user.watch_replied_threads = ThreadNotifications.SEND_EMAIL
    user.save()

    watched_thread = watched_thread_factory(
        user, thread, ThreadNotifications.DONT_EMAIL
    )

    watch_replied_thread(user, thread)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.notifications == ThreadNotifications.DONT_EMAIL


def test_replied_thread_watching_entry_is_not_removed_if_option_is_disabled(
    user, thread, watched_thread_factory
):
    user.watch_replied_threads = ThreadNotifications.NONE
    user.save()

    watched_thread = watched_thread_factory(
        user, thread, ThreadNotifications.DONT_EMAIL
    )

    watch_replied_thread(user, thread)

    watched_thread = WatchedThread.objects.get(user=user, thread=thread)
    assert watched_thread.notifications == ThreadNotifications.DONT_EMAIL
