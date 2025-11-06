from django.test import override_settings

from ..like import like_post


def test_like_post_creates_post_like_for_user(user, post):
    like = like_post(post, user)

    assert like.user == user
    assert like.user_name == user.username
    assert like.user_slug == user.slug


def test_like_post_creates_post_like_for_deleted_user(post):
    like = like_post(post, "DeletedUser")

    assert like.user is None
    assert like.user_name == "DeletedUser"
    assert like.user_slug == "deleteduser"


def test_like_post_updates_post_likes(post):
    post.likes = 12

    like_post(post, "DeletedUser")

    assert post.likes == 13

    post.refresh_from_db()
    assert post.likes == 13


def test_like_post_updates_post_last_likes_with_user_like(user, post):
    like_post(post, user)
    assert post.last_likes == [{"id": user.id, "username": user.username}]

    post.refresh_from_db()
    assert post.last_likes == [{"id": user.id, "username": user.username}]


def test_like_post_updates_post_last_likes_with_deleted_user_like(post):
    like_post(post, "DeletedUser")
    assert post.last_likes == [{"id": None, "username": "DeletedUser"}]

    post.refresh_from_db()
    assert post.last_likes == [{"id": None, "username": "DeletedUser"}]


def test_like_post_inserts_new_like_at_post_last_likes_beginning(user, post):
    post.last_likes = [
        {"id": 12, "username": "Lorem"},
        {"id": None, "username": "Ipsum"},
        {"id": 13, "username": "Dolor"},
    ]

    like_post(post, user)

    assert post.last_likes == [
        {"id": user.id, "username": user.username},
        {"id": 12, "username": "Lorem"},
        {"id": None, "username": "Ipsum"},
        {"id": 13, "username": "Dolor"},
    ]


@override_settings(MISAGO_POST_LAST_LIKES_LIMIT=3)
def test_like_post_trims_post_last_likes_to_setting_value(user, post):
    post.last_likes = [
        {"id": 12, "username": "Lorem"},
        {"id": None, "username": "Ipsum"},
        {"id": 13, "username": "Dolor"},
    ]

    like_post(post, user)

    assert post.last_likes == [
        {"id": user.id, "username": user.username},
        {"id": 12, "username": "Lorem"},
        {"id": None, "username": "Ipsum"},
    ]


def test_like_post_doesnt_save_changes_if_commit_is_false(
    django_assert_num_queries, user, post
):
    with django_assert_num_queries(0):
        like = like_post(post, user, commit=False)

    assert like.user == user
    assert like.user_name == user.username
    assert like.user_slug == user.slug

    assert post.likes == 1
    assert post.last_likes == [{"id": user.id, "username": user.username}]

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None
