from django.urls import reverse

from ..like import like_post
from ..models import Like


def test_thread_post_like_view_likes_post(user_client, user, thread, post):
    response = user_client.post(
        reverse(
            "misago:thread-post-like",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )

    assert response.status_code == 302

    assert Like.objects.filter(post=post, user=user).exists()

    post.refresh_from_db()
    assert post.likes == 1
    assert post.last_likes == [{"id": user.id, "username": user.username}]


def test_thread_post_like_view_does_nothing_for_already_liked_post(
    user_client, user, thread, post
):
    like = like_post(post, user)

    response = user_client.post(
        reverse(
            "misago:thread-post-like",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )

    assert response.status_code == 302

    assert Like.objects.filter(post=post, user=user).get() == like

    post.refresh_from_db()
    assert post.likes == 1
    assert post.last_likes == [{"id": user.id, "username": user.username}]
