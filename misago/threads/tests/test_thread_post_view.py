from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission


def test_thread_post_view_returns_redirect_to_post(
    thread_reply_factory, client, thread
):
    reply = thread_reply_factory(thread)

    response = client.get(
        reverse(
            "misago:thread-post",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": reply.id},
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


def test_thread_post_view_returns_error_404_if_thread_doesnt_exist(db, client):
    response = client.get(
        reverse(
            "misago:thread-post",
            kwargs={"thread_id": 1, "slug": "invalid", "post_id": 1},
        )
    )

    assert response.status_code == 404


def test_thread_post_view_returns_error_404_if_post_doesnt_exist(client, thread):
    response = client.get(
        reverse(
            "misago:thread-post",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": thread.first_post_id + 1,
            },
        )
    )

    assert response.status_code == 404


def test_thread_post_view_returns_error_404_if_user_cant_see_thread(
    thread_reply_factory, client, thread
):
    CategoryGroupPermission.objects.filter(
        category=thread.category,
        permission=CategoryPermission.BROWSE,
    ).delete()

    reply = thread_reply_factory(thread)

    response = client.get(
        reverse(
            "misago:thread-post",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": reply.id},
        )
    )

    assert response.status_code == 404


def test_thread_post_view_returns_error_403_if_user_cant_see_thread_contents(
    thread_reply_factory, client, thread
):
    thread.category.delay_browse_check = True
    thread.category.save()

    CategoryGroupPermission.objects.filter(
        category=thread.category,
        permission=CategoryPermission.BROWSE,
    ).delete()

    reply = thread_reply_factory(thread)

    response = client.get(
        reverse(
            "misago:thread-post",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": reply.id},
        )
    )

    assert response.status_code == 403


def test_thread_post_view_returns_error_404_if_user_cant_see_post(
    thread_reply_factory, client, thread
):
    reply = thread_reply_factory(thread, is_unapproved=True)

    response = client.get(
        reverse(
            "misago:thread-post",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": reply.id},
        )
    )

    assert response.status_code == 404


def test_thread_post_view_returns_error_404_if_thread_is_private(
    thread_reply_factory, user_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    response = user_client.get(
        reverse(
            "misago:thread-post",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": reply.id,
            },
        )
    )

    assert response.status_code == 404
