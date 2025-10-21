from datetime import timedelta

from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...notifications.users import notify_user
from ...readtracker.models import ReadCategory, ReadThread
from ...test import assert_contains


def test_thread_detail_view_doesnt_mark_unread_threads_for_guest(client, thread):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)

    assert not ReadCategory.objects.exists()
    assert not ReadThread.objects.exists()


def test_thread_detail_view_marks_category_as_read_for_user(
    user_client, user, default_category, thread
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    default_category.last_posted_at = thread.last_posted_at
    default_category.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)

    assert not ReadThread.objects.exists()
    ReadCategory.objects.get(
        user=user,
        category=default_category,
        read_time=default_category.last_posted_at,
    )


def test_thread_detail_view_marks_thread_as_read_for_user(
    user_client, user, default_category, thread, other_thread
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    default_category.last_posted_at = other_thread.last_posted_at
    default_category.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)

    assert not ReadCategory.objects.exists()
    ReadThread.objects.get(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=0)
def test_thread_detail_view_marks_unread_thread_posts_on_page_as_read_for_user(
    thread_factory, thread_reply_factory, user_client, user, default_category
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    thread = thread_factory(default_category, started_at=-900)

    posts = []
    for i in reversed(range(1, 6)):
        posted_at = i * 100 * -1
        posts.append(thread_reply_factory(thread, posted_at=posted_at))

    default_category.synchronize()
    default_category.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)

    assert not ReadCategory.objects.exists()
    ReadThread.objects.get(
        user=user,
        category=default_category,
        thread=thread,
        read_time=posts[-2].posted_at,
    )


def test_thread_detail_view_updates_user_watched_thread_read_time(
    user_client,
    user,
    default_category,
    old_thread,
    other_thread,
    watched_thread_factory,
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    watched_thread = watched_thread_factory(user, old_thread, False)
    watched_thread.read_time = watched_thread.read_time.replace(year=2010)
    watched_thread.save()

    default_category.last_posted_at = other_thread.last_posted_at
    default_category.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={"thread_id": old_thread.id, "slug": old_thread.slug},
        ),
    )
    assert_contains(response, old_thread.title)

    watched_thread.refresh_from_db()
    assert watched_thread.read_time == old_thread.last_posted_at


def test_thread_detail_view_marks_displayed_posts_notifications_as_read(
    user_client,
    user,
    default_category,
    thread,
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

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
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
    )
    assert_contains(response, thread.title)

    user.refresh_from_db()
    assert user.unread_notifications == 4

    notification.refresh_from_db()
    assert notification.is_read
