import pytest
from django.urls import reverse

from ...test import assert_contains
from ..like import like_post
from ..models import Like


def test_private_thread_post_unlike_view_removes_post_like(
    user_client, user, other_user_private_thread
):
    post = other_user_private_thread.first_post
    like = like_post(post, user)

    response = user_client.post(
        reverse(
            "misago:private-thread-post-unlike",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )

    assert response.status_code == 302

    with pytest.raises(Like.DoesNotExist):
        like.refresh_from_db()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_private_thread_post_unlike_view_does_nothing_for_not_liked_post(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    response = user_client.post(
        reverse(
            "misago:private-thread-post-unlike",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )

    assert response.status_code == 302

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_private_thread_post_unlike_view_removes_post_like_in_htmx(
    user_client, user, other_user_private_thread
):
    post = other_user_private_thread.first_post
    like = like_post(post, user)

    response = user_client.post(
        reverse(
            "misago:private-thread-post-unlike",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 200

    with pytest.raises(Like.DoesNotExist):
        like.refresh_from_db()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_private_thread_post_unlike_view_does_nothing_for_not_liked_post_in_htmx(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    response = user_client.post(
        reverse(
            "misago:private-thread-post-unlike",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 200

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_private_thread_post_like_view_returns_error_403_if_user_has_no_private_threads_permission(
    user_client, user, members_group, other_user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    post = other_user_private_thread.first_post

    response = user_client.post(
        reverse(
            "misago:private-thread-post-unlike",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )
    assert_contains(response, "You can&#x27;t use private threads.", status_code=403)

    assert not Like.objects.filter(post=post, user=user).exists()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_private_thread_post_like_view_returns_error_404_if_thread_doesnt_exist(
    user_client, user
):
    response = user_client.post(
        reverse(
            "misago:private-thread-post-unlike",
            kwargs={"thread_id": 100, "slug": "not-found", "post_id": 1},
        )
    )
    assert response.status_code == 404

    assert not Like.objects.filter(user=user).exists()


def test_private_thread_post_like_view_returns_error_404_if_thread_post_doesnt_exist(
    user_client, user, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-post-unlike",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": other_user_private_thread.last_post_id + 1,
            },
        )
    )
    assert response.status_code == 404

    assert not Like.objects.filter(user=user).exists()


def test_private_thread_post_like_view_returns_error_404_if_post_doesnt_exist_in_thread(
    user_client, user, user_private_thread, other_user_private_thread
):
    post = user_private_thread.first_post

    response = user_client.post(
        reverse(
            "misago:private-thread-post-unlike",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert response.status_code == 404

    assert not Like.objects.filter(post=post, user=user).exists()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_private_thread_post_like_view_returns_error_404_if_user_has_no_private_thread_access(
    user_client, user, private_thread
):
    post = private_thread.first_post

    response = user_client.post(
        reverse(
            "misago:private-thread-post-unlike",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
                "post_id": post.id,
            },
        ),
    )
    assert response.status_code == 404

    assert not Like.objects.filter(post=post, user=user).exists()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_private_thread_post_like_view_returns_error_403_if_user_is_anonymous(
    client, private_thread
):
    post = private_thread.first_post

    response = client.post(
        reverse(
            "misago:private-thread-post-unlike",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(
        response, "You must be signed in to use private threads.", status_code=403
    )

    assert not Like.objects.filter(post=post).exists()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_private_thread_post_like_view_returns_error_404_if_user_cant_like_posts(
    user_client, user, members_group, other_user_private_thread
):
    members_group.can_like_posts = False
    members_group.save()

    post = other_user_private_thread.first_post

    response = user_client.post(
        reverse(
            "misago:private-thread-post-unlike",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )
    assert_contains(
        response, "You can&#x27;t remove your like from this post.", status_code=403
    )

    assert not Like.objects.filter(post=post, user=user).exists()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_private_thread_post_like_view_returns_error_404_if_post_is_in_thread(
    user_client, user, thread, post
):
    response = user_client.post(
        reverse(
            "misago:private-thread-post-unlike",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert response.status_code == 404

    assert not Like.objects.filter(post=post, user=user).exists()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None
