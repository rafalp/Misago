from ..models import WatchedThread
from ..threads import ThreadNotifications, watch_new_private_thread


def test_private_thread_is_watched_with_email_notifications(user, private_thread):
    user.watch_new_private_threads_by_other_users = ThreadNotifications.SEND_EMAIL
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=False)

    assert watched_thread.user == user
    assert watched_thread.category == private_thread.category
    assert watched_thread.thread == private_thread
    assert watched_thread.notifications == ThreadNotifications.SEND_EMAIL
    assert watched_thread.read_at < private_thread.started_on

    WatchedThread.objects.get(
        user=user,
        thread=private_thread,
        notifications=ThreadNotifications.SEND_EMAIL,
    )


def test_private_thread_is_watched_without_email_notifications(user, private_thread):
    user.watch_new_private_threads_by_other_users = ThreadNotifications.DONT_EMAIL
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=False)

    assert watched_thread.user == user
    assert watched_thread.category == private_thread.category
    assert watched_thread.thread == private_thread
    assert watched_thread.notifications == ThreadNotifications.DONT_EMAIL
    assert watched_thread.read_at < private_thread.started_on

    WatchedThread.objects.get(
        user=user,
        thread=private_thread,
        notifications=ThreadNotifications.DONT_EMAIL,
    )


def test_private_thread_is_not_watched_with_notifications(user, private_thread):
    user.watch_new_private_threads_by_other_users = ThreadNotifications.NONE
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=False)

    assert watched_thread.user == user
    assert watched_thread.category == private_thread.category
    assert watched_thread.thread == private_thread
    assert watched_thread.notifications == ThreadNotifications.NONE
    assert watched_thread.read_at < private_thread.started_on

    WatchedThread.objects.get(
        user=user,
        thread=private_thread,
        notifications=ThreadNotifications.NONE,
    )


def test_private_thread_from_followed_is_watched_with_email_notifications(
    user, private_thread
):
    user.watch_new_private_threads_by_followed = ThreadNotifications.SEND_EMAIL
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=True)

    assert watched_thread.user == user
    assert watched_thread.category == private_thread.category
    assert watched_thread.thread == private_thread
    assert watched_thread.notifications == ThreadNotifications.SEND_EMAIL
    assert watched_thread.read_at < private_thread.started_on

    WatchedThread.objects.get(
        user=user,
        thread=private_thread,
        notifications=ThreadNotifications.SEND_EMAIL,
    )


def test_private_thread_from_followed_is_watched_without_email_notifications(
    user, private_thread
):
    user.watch_new_private_threads_by_followed = ThreadNotifications.DONT_EMAIL
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=True)

    assert watched_thread.user == user
    assert watched_thread.category == private_thread.category
    assert watched_thread.thread == private_thread
    assert watched_thread.notifications == ThreadNotifications.DONT_EMAIL
    assert watched_thread.read_at < private_thread.started_on

    WatchedThread.objects.get(
        user=user,
        thread=private_thread,
        notifications=ThreadNotifications.DONT_EMAIL,
    )


def test_private_thread_from_followed_is_not_watched_with_notifications(
    user, private_thread
):
    user.watch_new_private_threads_by_followed = ThreadNotifications.NONE
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=True)

    assert watched_thread.user == user
    assert watched_thread.category == private_thread.category
    assert watched_thread.thread == private_thread
    assert watched_thread.notifications == ThreadNotifications.NONE
    assert watched_thread.read_at < private_thread.started_on

    WatchedThread.objects.get(
        user=user,
        thread=private_thread,
        notifications=ThreadNotifications.NONE,
    )


def test_old_watched_thread_is_updated_instead_of_new_one_being_created(
    user, private_thread
):
    old_watched_thread = WatchedThread.objects.create(
        user=user,
        thread=private_thread,
        category=private_thread.category,
        notifications=ThreadNotifications.NONE,
    )

    user.watch_new_private_threads_by_other_users = ThreadNotifications.SEND_EMAIL
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=False)

    assert watched_thread.id == old_watched_thread.id
    assert watched_thread.user == user
    assert watched_thread.category == private_thread.category
    assert watched_thread.thread == private_thread
    assert watched_thread.notifications == ThreadNotifications.SEND_EMAIL
    assert watched_thread.read_at < private_thread.started_on
    assert watched_thread.read_at < old_watched_thread.read_at

    WatchedThread.objects.get(
        user=user,
        thread=private_thread,
    )


def test_old_watched_thread_notifications_are_not_disabled_by_new_preference(
    user, private_thread
):
    old_watched_thread = WatchedThread.objects.create(
        user=user,
        thread=private_thread,
        category=private_thread.category,
        notifications=ThreadNotifications.SEND_EMAIL,
    )

    user.watch_new_private_threads_by_other_users = ThreadNotifications.NONE
    user.save()

    watched_thread = watch_new_private_thread(user, private_thread, from_followed=False)

    assert watched_thread.id == old_watched_thread.id
    assert watched_thread.notifications == ThreadNotifications.SEND_EMAIL

    WatchedThread.objects.get(
        user=user,
        thread=private_thread,
    )
