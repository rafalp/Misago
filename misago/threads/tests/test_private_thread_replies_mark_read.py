from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...notifications.users import notify_user
from ...readtracker.models import ReadCategory, ReadThread
from ...test import assert_contains
from ..test import reply_thread


def test_private_thread_replies_view_marks_category_as_read_for_user(
    user_client, user, private_threads_category, user_private_thread
):
    private_threads_category.last_post_on = user_private_thread.last_post_on
    private_threads_category.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
    )
    assert_contains(response, user_private_thread.title)

    assert not ReadThread.objects.exists()
    ReadCategory.objects.get(
        user=user,
        category=private_threads_category,
        read_time=private_threads_category.last_post_on,
    )


def test_private_thread_replies_view_marks_thread_as_read_for_user(
    user_client,
    user,
    private_threads_category,
    user_private_thread,
    other_user_private_thread,
):
    private_threads_category.last_post_on = other_user_private_thread.last_post_on
    private_threads_category.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
    )
    assert_contains(response, user_private_thread.title)

    assert not ReadCategory.objects.exists()
    ReadThread.objects.get(
        user=user,
        category=private_threads_category,
        thread=user_private_thread,
        read_time=user_private_thread.last_post_on,
    )


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=0)
def test_private_thread_replies_view_marks_unread_thread_posts_on_page_as_read_for_user(
    user_client, user, private_threads_category, user_private_thread
):
    posts = [reply_thread(user_private_thread) for _ in range(5)]

    user_private_thread.synchronize()
    user_private_thread.save()

    private_threads_category.synchronize()
    private_threads_category.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
    )
    assert_contains(response, user_private_thread.title)

    assert not ReadCategory.objects.exists()
    ReadThread.objects.get(
        user=user,
        category=private_threads_category,
        thread=user_private_thread,
        read_time=posts[-2].posted_on,
    )


def test_private_thread_replies_view_updates_user_watched_thread_read_time(
    user_client,
    user,
    private_threads_category,
    user_private_thread,
    other_user_private_thread,
    watched_thread_factory,
):
    watched_thread = watched_thread_factory(user, user_private_thread, False)
    watched_thread.read_time = watched_thread.read_time.replace(year=2010)
    watched_thread.save()

    private_threads_category.last_post_on = other_user_private_thread.last_post_on
    private_threads_category.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
    )
    assert_contains(response, user_private_thread.title)

    watched_thread.refresh_from_db()
    assert watched_thread.read_time == user_private_thread.last_post_on


def test_private_thread_replies_view_marks_displayed_posts_notifications_as_read(
    user_client,
    user,
    private_threads_category,
    user_private_thread,
):
    notification = notify_user(
        user,
        "test",
        category=private_threads_category,
        thread=user_private_thread,
        post=user_private_thread.first_post,
    )

    user.unread_notifications = 5
    user.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
    )
    assert_contains(response, user_private_thread.title)

    user.refresh_from_db()
    assert user.unread_notifications == 4

    notification.refresh_from_db()
    assert notification.is_read


def test_private_thread_replies_view_decreases_user_unread_threads_count_on_thread_read(
    user_client,
    user,
    private_threads_category,
    user_private_thread,
    other_user_private_thread,
):
    user.unread_private_threads = 5
    user.save()

    private_threads_category.last_post_on = other_user_private_thread.last_post_on
    private_threads_category.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
    )
    assert_contains(response, user_private_thread.title)

    user.refresh_from_db()
    assert user.unread_private_threads == 4


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=0)
def test_private_thread_replies_view_doesnt_update_user_unread_threads_count_on_thread_page_read(
    user_client, user, private_threads_category, user_private_thread
):
    user.unread_private_threads = 5
    user.save()

    [reply_thread(user_private_thread) for _ in range(5)]

    private_threads_category.synchronize()
    private_threads_category.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
    )
    assert_contains(response, user_private_thread.title)

    user.refresh_from_db()
    assert user.unread_private_threads == 5


def test_private_thread_replies_view_clears_user_unread_threads_count_on_category_read(
    user_client, user, private_threads_category, user_private_thread
):
    user.unread_private_threads = 5
    user.save()

    private_threads_category.last_post_on = user_private_thread.last_post_on
    private_threads_category.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
    )
    assert_contains(response, user_private_thread.title)

    user.refresh_from_db()
    assert user.unread_private_threads == 0
