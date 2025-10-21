from django.urls import reverse


def test_private_thread_post_last_view_returns_redirect_to_last_post(
    thread_reply_factory, user_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    response = user_client.get(
        reverse(
            "misago:private-thread-post-last",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
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


def test_private_thread_post_last_view_returns_error_404_if_thread_doesnt_exist(
    user_client,
):
    response = user_client.get(
        reverse(
            "misago:private-thread-post-last",
            kwargs={"thread_id": 1, "slug": "invalid"},
        )
    )

    assert response.status_code == 404


def test_private_thread_post_last_view_returns_error_403_if_user_cant_use_private_threads(
    user_client, members_group, user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-post-last",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )

    assert response.status_code == 403


def test_private_thread_post_last_view_returns_error_404_if_user_cant_see_thread(
    user_client, private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-post-last",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        )
    )

    assert response.status_code == 404


def test_private_thread_post_last_view_returns_error_if_thread_is_public(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-post-last",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert response.status_code == 404
