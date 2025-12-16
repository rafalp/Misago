from ..models import Like
from ..synchronize import synchronize_post_likes


def test_synchronize_post_likes_synchronizes_post_without_likes(post):
    synchronize_post_likes(post)

    assert post.likes == 0
    assert post.last_likes is None

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_synchronize_post_likes_synchronizes_post_without_likes_with_invalid_likes_count(
    post,
):
    post.likes = 42
    post.save()

    synchronize_post_likes(post)

    assert post.likes == 0
    assert post.last_likes is None

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_synchronize_post_likes_synchronizes_post_without_likes_with_invalid_last_likes(
    post,
):
    post.last_likes = ["a", "b", "c"]
    post.save()

    synchronize_post_likes(post)

    assert post.likes == 0
    assert post.last_likes is None

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_synchronize_post_likes_synchronizes_post_without_likes_with_invalid_last_likes_and_count(
    post,
):
    post.likes = 42
    post.last_likes = ["a", "b", "c"]
    post.save()

    synchronize_post_likes(post)

    assert post.likes == 0
    assert post.last_likes is None

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None


def test_synchronize_post_likes_synchronizes_post_with_likes_with_invalid_last_likes_and_count(
    post, user
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

    post.likes = 42
    post.last_likes = ["a", "b", "c"]
    post.save()

    synchronize_post_likes(post)

    assert post.likes == 2
    assert post.last_likes == [
        {"id": None, "username": "DeletedUser"},
        {"id": user.id, "username": user.username},
    ]

    post.refresh_from_db()
    assert post.likes == 2
    assert post.last_likes == [
        {"id": None, "username": "DeletedUser"},
        {"id": user.id, "username": user.username},
    ]


def test_synchronize_post_likes_uses_custom_queryset(user, other_user, post):
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
        user=other_user,
        user_name=other_user.username,
        user_slug=other_user.slug,
    )

    Like.objects.create(
        category_id=post.category_id,
        thread_id=post.thread_id,
        post=post,
        user_name="DeletedUser",
        user_slug="deleteduser",
    )

    synchronize_post_likes(post, Like.objects.exclude(user=other_user))

    assert post.likes == 2
    assert post.last_likes == [
        {"id": None, "username": "DeletedUser"},
        {"id": user.id, "username": user.username},
    ]

    post.refresh_from_db()
    assert post.likes == 2
    assert post.last_likes == [
        {"id": None, "username": "DeletedUser"},
        {"id": user.id, "username": user.username},
    ]


def test_synchronize_post_likes_doesnt_commit_if_commit_is_false(
    django_assert_num_queries, post
):
    post.likes = 42
    post.last_likes = ["a", "b", "c"]
    post.save()

    with django_assert_num_queries(1):
        synchronize_post_likes(post, queryset=None, commit=False)

    assert post.likes == 0
    assert post.last_likes is None

    post.refresh_from_db()
    post.likes = 42
    post.last_likes = ["a", "b", "c"]
