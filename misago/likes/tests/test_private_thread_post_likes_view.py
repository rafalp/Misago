from django.urls import reverse

from ...test import assert_contains, assert_not_contains
from ..like import like_post


def test_private_thread_post_likes_view_shows_empty(user_client, user_private_thread):
    post = user_private_thread.first_post

    response = user_client.get(
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "This post has no likes.")


def test_private_thread_post_likes_view_shows_empty_in_htmx(
    user_client, user_private_thread
):
    post = user_private_thread.first_post

    response = user_client.get(
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no likes.")


def test_private_thread_post_likes_view_shows_empty_in_modal(
    user_client, user_private_thread
):
    post = user_private_thread.first_post

    response = user_client.get(
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no likes.")


def test_private_thread_post_likes_view_shows_user_like(
    user_client, other_user, user_private_thread
):
    post = user_private_thread.first_post

    like_post(post, other_user)

    response = user_client.get(
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, other_user.username)


def test_private_thread_post_likes_view_shows_deleted_user_like(
    user_client, user_private_thread
):
    post = user_private_thread.first_post

    like_post(post, "DeletedUser")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "DeletedUser")


def test_private_thread_post_likes_view_shows_user_like_in_modal(
    user_client, other_user, user_private_thread
):
    post = user_private_thread.first_post

    like_post(post, other_user)

    response = user_client.get(
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, other_user.username)


def test_private_thread_post_likes_view_shows_deleted_user_like_in_modal(
    user_client, user_private_thread
):
    post = user_private_thread.first_post

    like_post(post, "DeletedUser")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "DeletedUser")


def test_private_thread_post_likes_view_displays_another_page_of_results(
    user_client, user_private_thread
):
    post = user_private_thread.first_post

    for i in range(1, 41):
        like_post(post, f"User{i}")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
    )
    assert_not_contains(response, "User40")
    assert_contains(response, "User1")


def test_private_thread_post_likes_view_displays_another_page_of_results_in_htmx(
    user_client, user_private_thread
):
    post = user_private_thread.first_post

    for i in range(1, 41):
        like_post(post, f"User{i}")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "User40")
    assert_contains(response, "User1")


def test_private_thread_post_likes_view_displays_another_page_of_results_in_modal(
    user_client, user_private_thread
):
    post = user_private_thread.first_post

    for i in range(1, 20):
        like_post(post, f"User{i}")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "User10")
    assert_contains(response, "User1")


def test_private_thread_post_likes_view_redirects_from_out_of_range_last_page(
    user_client, user_private_thread
):
    post = user_private_thread.first_post

    response = user_client.get(
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
                "page": 3,
            },
        )
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread-post-likes",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "post_id": post.id,
        },
    )


def test_private_thread_post_likes_view_displays_last_page_from_out_of_range_last_page_in_htmx(
    user_client, user_private_thread
):
    post = user_private_thread.first_post

    like_post(post, "DeletedUser")

    response = user_client.get(
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
                "page": 3,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "DeletedUser")
