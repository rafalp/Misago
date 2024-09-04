from django.urls import reverse
from django.utils import timezone

from ...readtracker.models import ReadCategory
from ...readtracker.tracker import mark_thread_read
from ..test import reply_thread


def test_thread_last_post_redirect_view_returns_redirect(client, thread):
    reply = reply_thread(thread)

    response = client.get(
        reverse(
            "misago:thread-last-post",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_private_thread_last_post_redirect_view_returns_redirect(
    user_client, user_private_thread
):
    reply = reply_thread(user_private_thread)

    response = user_client.get(
        reverse(
            "misago:private-thread-last-post",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_thread_unread_post_redirect_view_returns_redirect_to_last_post_for_anonymous_user(
    client, thread
):
    reply_thread(thread, posted_on=timezone.now())
    reply = reply_thread(thread, posted_on=timezone.now())

    response = client.get(
        reverse(
            "misago:thread-unread-post",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_thread_unread_post_redirect_view_returns_redirect_to_first_unread_post_for_user(
    user, user_client, thread
):
    mark_thread_read(user, thread, thread.first_post.posted_on)

    reply = reply_thread(thread, posted_on=timezone.now())
    reply_thread(thread, posted_on=timezone.now())

    response = user_client.get(
        reverse(
            "misago:thread-unread-post",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_thread_unread_post_redirect_view_returns_redirect_to_last_post_for_read_thread(
    user, user_client, thread
):
    reply_thread(thread, posted_on=timezone.now())
    reply = reply_thread(thread, posted_on=timezone.now())

    mark_thread_read(user, thread, timezone.now())

    response = user_client.get(
        reverse(
            "misago:thread-unread-post",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_thread_unread_post_redirect_view_returns_redirect_to_last_post_for_read_category(
    user, user_client, thread
):
    reply_thread(thread, posted_on=timezone.now())
    reply = reply_thread(thread, posted_on=timezone.now())

    ReadCategory.objects.create(
        user=user,
        category=thread.category,
        read_time=timezone.now(),
    )

    response = user_client.get(
        reverse(
            "misago:thread-unread-post",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_private_thread_unread_post_redirect_view_returns_error_404_for_anonymous_client(
    client, user_private_thread
):
    response = client.get(
        reverse(
            "misago:private-thread-unread-post",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )

    assert response.status_code == 403


def test_private_thread_unread_post_redirect_view_returns_redirect_to_first_unread_post_for_user(
    user, user_client, user_private_thread
):
    mark_thread_read(
        user, user_private_thread, user_private_thread.first_post.posted_on
    )

    reply = reply_thread(user_private_thread, posted_on=timezone.now())
    reply_thread(user_private_thread, posted_on=timezone.now())

    response = user_client.get(
        reverse(
            "misago:private-thread-unread-post",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_private_thread_unread_post_redirect_view_returns_redirect_to_last_post_for_read_thread(
    user, user_client, user_private_thread
):
    reply_thread(user_private_thread, posted_on=timezone.now())
    reply = reply_thread(user_private_thread, posted_on=timezone.now())

    mark_thread_read(user, user_private_thread, timezone.now())

    response = user_client.get(
        reverse(
            "misago:private-thread-unread-post",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_private_thread_unread_post_redirect_view_returns_redirect_to_last_post_for_read_category(
    user, user_client, user_private_thread
):
    reply_thread(user_private_thread, posted_on=timezone.now())
    reply = reply_thread(user_private_thread, posted_on=timezone.now())

    ReadCategory.objects.create(
        user=user,
        category=user_private_thread.category,
        read_time=timezone.now(),
    )

    response = user_client.get(
        reverse(
            "misago:private-thread-unread-post",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
        + f"#post-{reply.id}"
    )
