from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains


def test_thread_post_unapproved_view_returns_redirect_to_first_unapproved_post(
    thread_reply_factory, moderator_client, thread
):
    reply = thread_reply_factory(thread, is_unapproved=True)
    thread_reply_factory(thread, is_unapproved=True)
    thread_reply_factory(thread)

    response = moderator_client.get(
        reverse(
            "misago:thread-post-unapproved",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_thread_post_unapproved_view_returns_redirect_to_last_post_for_thread_without_unapproved_posts(
    thread_reply_factory, moderator_client, thread
):
    thread_reply_factory(thread)
    thread_reply_factory(thread)
    reply = thread_reply_factory(thread)

    response = moderator_client.get(
        reverse(
            "misago:thread-post-unapproved",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_thread_post_unapproved_view_returns_error_404_if_thread_doesnt_exist(
    moderator_client,
):
    response = moderator_client.get(
        reverse(
            "misago:thread-post-unapproved",
            kwargs={"thread_id": 1, "slug": "invalid"},
        )
    )

    assert response.status_code == 404


def test_thread_post_unapproved_view_returns_error_404_if_user_cant_see_thread(
    moderator_client, thread
):
    CategoryGroupPermission.objects.filter(
        category=thread.category,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = moderator_client.get(
        reverse(
            "misago:thread-post-unapproved",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 404


def test_thread_post_unapproved_view_returns_error_403_if_user_cant_see_thread_contents(
    moderator_client, thread
):
    thread.category.delay_browse_check = True
    thread.category.save()

    CategoryGroupPermission.objects.filter(
        category=thread.category,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = moderator_client.get(
        reverse(
            "misago:thread-post-unapproved",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 403


def test_thread_post_unapproved_view_returns_error_403_if_user_cant_moderate_thread(
    client, thread
):
    response = client.get(
        reverse(
            "misago:thread-post-unapproved",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert_contains(response, "You must be a moderator to view unapproved posts.", 403)


def test_thread_post_unapproved_view_returns_error_404_if_thread_is_private(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:thread-post-unapproved",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )

    assert response.status_code == 404
