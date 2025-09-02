from django.urls import reverse

from ...threads.test import reply_thread


def test_post_redirect_view_returns_404_for_not_existing_post_id(client, thread):
    reply = reply_thread(thread)

    response = client.get(reverse("misago:post", kwargs={"id": reply.id + 10}))
    assert response.status_code == 404


def test_post_redirect_view_returns_error_404_if_user_cant_see_private_thread(
    user_client, private_thread
):
    reply = reply_thread(private_thread)

    response = user_client.get(reverse("misago:post", kwargs={"id": reply.id}))
    assert response.status_code == 404


def test_post_redirect_view_returns_redirect_to_thread_post(client, thread):
    reply = reply_thread(thread)

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
    user_client, user_private_thread
):
    reply = reply_thread(user_private_thread)

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
    client, thread
):
    reply = reply_thread(thread)

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
    user_client, user_private_thread
):
    reply = reply_thread(user_private_thread)

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
