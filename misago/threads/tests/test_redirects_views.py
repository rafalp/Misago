from django.urls import reverse
from django.utils import timezone

from ...readtracker.models import ReadCategory
from ...readtracker.tracker import mark_thread_read
from ...test import assert_contains


def test_thread_last_post_redirect_view_returns_redirect(
    thread_reply_factory, client, thread
):
    reply = thread_reply_factory(thread)

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
    thread_reply_factory, user_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

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
    thread_reply_factory, client, thread
):
    thread_reply_factory(thread)
    reply = thread_reply_factory(thread)

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
    thread_reply_factory, user, user_client, thread
):
    mark_thread_read(user, thread, thread.first_post.posted_at)

    reply = thread_reply_factory(thread)
    thread_reply_factory(thread)

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
    thread_reply_factory, user, user_client, thread
):
    thread_reply_factory(thread)
    reply = thread_reply_factory(thread)

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
    thread_reply_factory, user, user_client, thread
):
    thread_reply_factory(thread)
    reply = thread_reply_factory(thread)

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
    thread_reply_factory, user, user_client, user_private_thread
):
    mark_thread_read(
        user, user_private_thread, user_private_thread.first_post.posted_at
    )

    reply = thread_reply_factory(user_private_thread)
    thread_reply_factory(user_private_thread)

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
    thread_reply_factory, user, user_client, user_private_thread
):
    thread_reply_factory(user_private_thread)
    reply = thread_reply_factory(user_private_thread)

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
    thread_reply_factory, user, user_client, user_private_thread
):
    thread_reply_factory(user_private_thread)
    reply = thread_reply_factory(user_private_thread)

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


def test_thread_solution_redirect_view_returns_redirect_to_solution_post(
    thread_reply_factory, client, thread
):
    solution = thread_reply_factory(thread)
    thread_reply_factory(thread)

    thread.best_answer = solution
    thread.save()

    response = client.get(
        reverse(
            "misago:thread-solution-post",
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
        + f"#post-{solution.id}"
    )


def test_thread_solution_redirect_view_returns_redirect_to_last_post_in_unsolved_thread(
    thread_reply_factory, client, thread
):
    thread_reply_factory(thread)
    reply = thread_reply_factory(thread)

    response = client.get(
        reverse(
            "misago:thread-solution-post",
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


def test_thread_unapproved_redirect_view_returns_error_for_anonymous_user(
    client, thread
):
    response = client.get(
        reverse(
            "misago:thread-unapproved-post",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )
    assert_contains(
        response,
        "You must be a moderator to view unapproved posts.",
        status_code=403,
    )


def test_thread_unapproved_redirect_view_returns_error_for_user_without_moderator_permission(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:thread-unapproved-post",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )
    assert_contains(
        response,
        "You must be a moderator to view unapproved posts.",
        status_code=403,
    )


def test_thread_unapproved_redirect_view_redirects_moderator_to_last_post_if_no_unapproved_posts_exist(
    thread_reply_factory, moderator_client, thread
):
    reply = thread_reply_factory(thread)

    response = moderator_client.get(
        reverse(
            "misago:thread-unapproved-post",
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


def test_thread_unapproved_redirect_view_redirects_moderator_to_unapproved_post(
    thread_reply_factory, moderator_client, thread
):
    unapproved = thread_reply_factory(thread, is_unapproved=True)
    thread_reply_factory(thread)

    response = moderator_client.get(
        reverse(
            "misago:thread-unapproved-post",
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
        + f"#post-{unapproved.id}"
    )


def test_private_thread_unapproved_redirect_view_returns_error_for_user_without_moderator_permission(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-unapproved-post",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_contains(
        response,
        "You must be a moderator to view unapproved posts.",
        status_code=403,
    )


def test_private_thread_unapproved_redirect_view_redirects_moderator_to_last_post_if_no_unapproved_posts_exist(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    response = moderator_client.get(
        reverse(
            "misago:private-thread-unapproved-post",
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


def test_private_thread_unapproved_redirect_view_redirects_moderator_to_unapproved_post(
    thread_reply_factory, moderator_client, user_private_thread
):
    unapproved = thread_reply_factory(user_private_thread, is_unapproved=True)
    thread_reply_factory(user_private_thread)

    response = moderator_client.get(
        reverse(
            "misago:private-thread-unapproved-post",
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
        + f"#post-{unapproved.id}"
    )


def test_post_redirect_view_returns_404_for_not_existing_post_id(
    thread_reply_factory, client, thread
):
    reply = thread_reply_factory(thread)

    response = client.get(reverse("misago:post", kwargs={"id": reply.id + 10}))
    assert response.status_code == 404


def test_post_redirect_view_returns_error_404_if_user_cant_see_private_thread(
    thread_reply_factory, user_client, private_thread
):
    reply = thread_reply_factory(private_thread)

    response = user_client.get(reverse("misago:post", kwargs={"id": reply.id}))
    assert response.status_code == 404


def test_post_redirect_view_returns_redirect_to_thread_post(
    thread_reply_factory, client, thread
):
    reply = thread_reply_factory(thread)

    response = client.get(reverse("misago:post", kwargs={"id": reply.id}))

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_post_redirect_view_returns_redirect_to_private_thread_post(
    thread_reply_factory, user_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    response = user_client.get(reverse("misago:post", kwargs={"id": reply.id}))

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_post_redirect_view_returns_redirect_to_thread_post_for_post_request(
    thread_reply_factory, client, thread
):
    reply = thread_reply_factory(thread)

    response = client.post(reverse("misago:post", kwargs={"id": reply.id}))

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_post_redirect_view_returns_redirect_to_private_thread_post_for_post_request(
    thread_reply_factory, user_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    response = user_client.post(reverse("misago:post", kwargs={"id": reply.id}))

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
        + f"#post-{reply.id}"
    )
