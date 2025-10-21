from django.urls import reverse


def test_private_thread_post_view_returns_redirect_to_post(
    thread_reply_factory, user_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    response = user_client.get(
        reverse(
            "misago:private-thread-post",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": reply.id,
            },
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )


def test_private_thread_post_view_returns_error_404_if_thread_doesnt_exist(user_client):
    response = user_client.get(
        reverse(
            "misago:private-thread-post",
            kwargs={"thread_id": 1, "slug": "invalid", "post_id": 1},
        )
    )

    assert response.status_code == 404


def test_private_thread_post_view_returns_error_404_if_post_doesnt_exist(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-post",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.id,
                "post_id": user_private_thread.first_post_id + 1,
            },
        )
    )

    assert response.status_code == 404


def test_private_thread_post_view_returns_error_403_if_user_cant_use_private_threads(
    thread_reply_factory, user_client, members_group, user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    reply = thread_reply_factory(user_private_thread)

    response = user_client.get(
        reverse(
            "misago:private-thread-post",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": reply.id,
            },
        )
    )

    assert response.status_code == 403


def test_private_thread_post_view_returns_error_404_if_user_cant_see_thread(
    thread_reply_factory, user_client, private_thread
):
    reply = thread_reply_factory(private_thread)

    response = user_client.get(
        reverse(
            "misago:private-thread-post",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
                "post_id": reply.id,
            },
        )
    )

    assert response.status_code == 404


def test_private_thread_post_view_returns_error_if_thread_is_public(
    thread_reply_factory, user_client, thread
):
    reply = thread_reply_factory(thread)

    response = user_client.get(
        reverse(
            "misago:private-thread-post",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": reply.id,
            },
        )
    )

    assert response.status_code == 404
