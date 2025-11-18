from unittest.mock import Mock

from ..postfeed import get_post_feed_post_likes_data


def test_get_post_feed_post_likes_data_returns_data_for_unliked_post_without_likes(
    user, user_permissions, post
):
    request = Mock(user=user, user_permissions=user_permissions)
    data = get_post_feed_post_likes_data(
        request, post, False, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 0,
        "description": None,
        "is_liked": False,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }
