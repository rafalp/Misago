from ..models import WatchedThread
from ..threads import ThreadNotifications, watch_new_private_thread


def test_private_thread_is_watched_with_email_notifications(user, private_thread):
    user.watch_new_private_threads_by_other_users = ThreadNotifications.SITE_AND_EMAIL
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=False)

    assert watched_thread.user == user
    assert watched_thread.category == private_thread.category
    assert watched_thread.thread == private_thread
    assert watched_thread.send_emails
    assert watched_thread.read_time < private_thread.started_on

    WatchedThread.objects.get(
        user=user,
        thread=private_thread,
        send_emails=True,
    )


def test_private_thread_is_watched_without_email_notifications(user, private_thread):
    user.watch_new_private_threads_by_other_users = ThreadNotifications.SITE_ONLY
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=False)

    assert watched_thread.user == user
    assert watched_thread.category == private_thread.category
    assert watched_thread.thread == private_thread
    assert not watched_thread.send_emails
    assert watched_thread.read_time < private_thread.started_on

    WatchedThread.objects.get(
        user=user,
        thread=private_thread,
        send_emails=False,
    )


def test_private_thread_is_not_watched(user, private_thread):
    user.watch_new_private_threads_by_other_users = ThreadNotifications.NONE
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=False)
    assert watched_thread is None

    assert not WatchedThread.objects.exists()


def test_private_thread_from_followed_is_watched_with_email_notifications(
    user, private_thread
):
    user.watch_new_private_threads_by_followed = ThreadNotifications.SITE_AND_EMAIL
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=True)

    assert watched_thread.user == user
    assert watched_thread.category == private_thread.category
    assert watched_thread.thread == private_thread
    assert watched_thread.send_emails
    assert watched_thread.read_time < private_thread.started_on

    WatchedThread.objects.get(
        user=user,
        thread=private_thread,
        send_emails=True,
    )


def test_private_thread_from_followed_is_watched_without_email_notifications(
    user, private_thread
):
    user.watch_new_private_threads_by_followed = ThreadNotifications.SITE_ONLY
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=True)

    assert watched_thread.user == user
    assert watched_thread.category == private_thread.category
    assert watched_thread.thread == private_thread
    assert not watched_thread.send_emails
    assert watched_thread.read_time < private_thread.started_on

    WatchedThread.objects.get(
        user=user,
        thread=private_thread,
        send_emails=False,
    )


def test_private_thread_from_followed_is_not_watched(user, private_thread):
    user.watch_new_private_threads_by_followed = ThreadNotifications.NONE
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=True)
    assert watched_thread is None

    assert not WatchedThread.objects.exists()


def test_old_watched_thread_notifications_are_not_disabled_by_new_preference(
    user, private_thread
):
    old_watched_thread = WatchedThread.objects.create(
        user=user,
        thread=private_thread,
        category=private_thread.category,
        send_emails=True,
    )

    user.watch_new_private_threads_by_other_users = ThreadNotifications.SITE_ONLY
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=False)

    assert watched_thread.id == old_watched_thread.id
    assert watched_thread.send_emails

    WatchedThread.objects.get(
        user=user,
        thread=private_thread,
        send_emails=True,
    )
