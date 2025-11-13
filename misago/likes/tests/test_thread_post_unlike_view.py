import pytest
from django.urls import reverse

from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains
from ..like import like_post
from ..models import Like


def test_thread_post_unlike_view_removes_post_like(user_client, user, thread, post):
    like = like_post(post, user)

    response = user_client.post(
        reverse(
            "misago:thread-post-unlike",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )

    assert response.status_code == 302

    with pytest.raises(Like.DoesNotExist):
        like.refresh_from_db()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_thread_post_unlike_view_does_nothing_for_not_liked_post(
    user_client, thread, post
):
    response = user_client.post(
        reverse(
            "misago:thread-post-unlike",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )

    assert response.status_code == 302

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_thread_post_unlike_view_removes_post_like_in_htmx(
    user_client, user, thread, post
):
    like = like_post(post, user)

    response = user_client.post(
        reverse(
            "misago:thread-post-unlike",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 200

    with pytest.raises(Like.DoesNotExist):
        like.refresh_from_db()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_thread_post_unlike_view_does_nothing_for_not_liked_post_in_htmx(
    user_client, thread, post
):
    response = user_client.post(
        reverse(
            "misago:thread-post-unlike",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        ),
        headers={"hx-request": "true"},
    )

    assert response.status_code == 200

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_thread_post_unlike_view_returns_error_404_if_thread_doesnt_exist(
    user_client, user
):
    response = user_client.post(
        reverse(
            "misago:thread-post-unlike",
            kwargs={"thread_id": 100, "slug": "not-found", "post_id": 1},
        )
    )
    assert response.status_code == 404

    assert not Like.objects.filter(user=user).exists()


def test_thread_post_unlike_view_returns_error_404_if_thread_post_doesnt_exist(
    user_client, user, thread
):
    response = user_client.post(
        reverse(
            "misago:thread-post-unlike",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": thread.last_post_id + 1,
            },
        )
    )
    assert response.status_code == 404

    assert not Like.objects.filter(user=user).exists()


def test_thread_post_unlike_view_returns_error_404_if_post_doesnt_exist_in_thread(
    user_client, user, thread, user_thread
):
    post = user_thread.first_post

    response = user_client.post(
        reverse(
            "misago:thread-post-unlike",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert response.status_code == 404

    assert not Like.objects.filter(post=post, user=user).exists()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_thread_post_unlike_view_returns_error_404_if_user_has_no_category_permission(
    user_client, user, thread, post
):
    CategoryGroupPermission.objects.filter(category=thread.category).delete()

    response = user_client.post(
        reverse(
            "misago:thread-post-unlike",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert response.status_code == 404

    assert not Like.objects.filter(post=post, user=user).exists()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_thread_post_unlike_view_returns_error_404_if_user_has_no_thread_permission(
    user_client, user, thread, post
):
    thread.is_unapproved = True
    thread.save()

    response = user_client.post(
        reverse(
            "misago:thread-post-unlike",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert response.status_code == 404

    assert not Like.objects.filter(post=post, user=user).exists()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_thread_post_unlike_view_returns_error_404_if_user_has_no_post_permission(
    user_client, user, thread, post
):
    post.is_unapproved = True
    post.save()

    response = user_client.post(
        reverse(
            "misago:thread-post-unlike",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert response.status_code == 404

    assert not Like.objects.filter(post=post, user=user).exists()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_thread_post_unlike_view_returns_error_403_if_user_is_anonymous(
    client, thread, post
):
    response = client.post(
        reverse(
            "misago:thread-post-unlike",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert_contains(response, "You can&#x27;t remove posts likes.", status_code=403)

    assert not Like.objects.filter(post=post).exists()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_thread_post_unlike_view_returns_error_403_if_user_cant_like_posts(
    user_client, user, members_group, thread, post
):
    members_group.can_like_posts = False
    members_group.save()

    response = user_client.post(
        reverse(
            "misago:thread-post-unlike",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert_contains(
        response, "You can&#x27;t remove your like from this post.", status_code=403
    )

    assert not Like.objects.filter(post=post, user=user).exists()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_thread_post_unlike_view_returns_error_404_if_post_is_in_private_thread(
    user_client, user, other_user_private_thread
):
    post = other_user_private_thread.first_post

    response = user_client.post(
        reverse(
            "misago:thread-post-unlike",
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
