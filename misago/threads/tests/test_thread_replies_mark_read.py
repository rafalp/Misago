from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...notifications.users import notify_user
from ...readtracker.models import ReadCategory, ReadThread
from ...test import assert_contains
from ..test import reply_thread


def test_thread_replies_view_doesnt_mark_unread_threads_for_guest(client, thread):
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)

    assert not ReadCategory.objects.exists()
    assert not ReadThread.objects.exists()


def test_thread_replies_view_marks_category_as_read_for_user(
    user_client, user, default_category, thread
):
    default_category.last_post_on = thread.last_post_on
    default_category.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)

    assert not ReadThread.objects.exists()
    ReadCategory.objects.get(
        user=user,
        category=default_category,
        read_time=default_category.last_post_on,
    )


def test_thread_replies_view_marks_thread_as_read_for_user(
    user_client, user, default_category, thread, other_thread
):
    default_category.last_post_on = other_thread.last_post_on
    default_category.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)

    assert not ReadCategory.objects.exists()
    ReadThread.objects.get(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_post_on,
    )


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=0)
def test_thread_replies_view_marks_unread_thread_posts_on_page_as_read_for_user(
    user_client, user, default_category, thread
):
    posts = [reply_thread(thread) for _ in range(5)]

    thread.synchronize()
    thread.save()

    default_category.synchronize()
    default_category.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)

    assert not ReadCategory.objects.exists()
    ReadThread.objects.get(
        user=user,
        category=default_category,
        thread=thread,
        read_time=posts[-2].posted_on,
    )


def test_thread_replies_view_updates_user_watched_thread_read_time(
    user_client,
    user,
    default_category,
    thread,
    other_thread,
    watched_thread_factory,
):
    watched_thread = watched_thread_factory(user, thread, False)
    watched_thread.read_time = watched_thread.read_time.replace(year=2010)
    watched_thread.save()

    default_category.last_post_on = other_thread.last_post_on
    default_category.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)

    watched_thread.refresh_from_db()
    assert watched_thread.read_time == thread.last_post_on


def test_thread_replies_view_marks_displayed_posts_notifications_as_read(
    user_client,
    user,
    default_category,
    thread,
):
    notification = notify_user(
        user,
        "test",
        category=default_category,
        thread=thread,
        post=thread.first_post,
    )

    user.unread_notifications = 5
    user.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
    )
    assert_contains(response, thread.title)

    user.refresh_from_db()
    assert user.unread_notifications == 4

    notification.refresh_from_db()
    assert notification.is_read
