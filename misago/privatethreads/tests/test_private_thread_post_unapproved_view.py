from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains


def test_private_thread_post_unapproved_view_returns_redirect_to_first_unapproved_post(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, is_unapproved=True)
    thread_reply_factory(user_private_thread, is_unapproved=True)

    response = moderator_client.get(
        reverse(
            "misago:private-thread-post-unapproved",
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


def test_private_thread_post_unapproved_view_returns_redirect_to_last_post_for_thread_without_unapproved_posts(
    thread_reply_factory, moderator_client, user_private_thread
):
    thread_reply_factory(user_private_thread)
    thread_reply_factory(user_private_thread)
    reply = thread_reply_factory(user_private_thread)

    response = moderator_client.get(
        reverse(
            "misago:private-thread-post-unapproved",
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


def test_private_thread_post_unapproved_view_returns_error_404_if_thread_doesnt_exist(
    moderator_client,
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread-post-unapproved",
            kwargs={"id": 1, "slug": "invalid"},
        )
    )

    assert response.status_code == 404


def test_private_thread_post_last_view_returns_error_403_if_user_cant_use_private_threads(
    moderator_client, moderators_group, user_private_thread
):
    moderators_group.can_use_private_threads = False
    moderators_group.save()

    response = moderator_client.get(
        reverse(
            "misago:private-thread-post-last",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )

    assert response.status_code == 403


def test_private_thread_post_unapproved_view_returns_error_404_if_user_cant_see_thread(
    moderator_client, private_thread
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread-post-unapproved",
            kwargs={"id": private_thread.id, "slug": private_thread.slug},
        )
    )

    assert response.status_code == 404


def test_private_thread_post_unapproved_view_returns_error_403_if_user_cant_moderate_thread(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-post-unapproved",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_contains(response, "You must be a moderator to view unapproved posts.", 403)
