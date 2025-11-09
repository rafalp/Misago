import pytest

from ..like import remove_post_like
from ..models import Like


def test_remove_post_like_does_nothing_if_no_like_was_deleted(
    django_assert_num_queries, user, post
):
    with django_assert_num_queries(1):
        assert not remove_post_like(post, user)


def test_remove_post_like_deletes_post_like_by_user(
    django_assert_num_queries, user, post
):
    Like.objects.create(
        category_id=post.category_id,
        thread_id=post.thread_id,
        post=post,
        user=user,
        user_name=user.username,
        user_slug=user.slug,
    )

    Like.objects.create(
        category_id=post.category_id,
        thread_id=post.thread_id,
        post=post,
        user_name="DeletedUser",
        user_slug="deleteduser",
    )

    with django_assert_num_queries(4):
        assert remove_post_like(post, user)

    with pytest.raises(Like.DoesNotExist):
        Like.objects.get(post=post, user=user)

    assert post.likes == 1
    assert post.last_likes == [{"id": None, "username": "DeletedUser"}]

    post.refresh_from_db()
    assert post.likes == 1
    assert post.last_likes == [{"id": None, "username": "DeletedUser"}]
