from django.urls import reverse

from ..test import reply_thread


def test_thread_last_post_redirect_view_returns_redirect_link(client, thread):
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


def test_private_thread_last_post_redirect_view_returns_redirect_link(
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
