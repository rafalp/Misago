from unittest.mock import Mock

from ...permissions.enums import CanSeePostLikes
from ..like import like_post
from ..postfeed import get_post_feed_post_likes_data


def test_get_post_feed_post_likes_data_for_unliked_post_without_likes(
    user, user_permissions, post
):
    request = Mock(user=user, user_permissions=user_permissions)
    data = get_post_feed_post_likes_data(
        request, post, False, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 0,
        "messages": None,
        "is_liked": False,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_unliked_post_without_likes_for_user_without_last_likes_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    data = get_post_feed_post_likes_data(
        request, post, False, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 0,
        "messages": None,
        "is_liked": False,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_unliked_post_without_likes_for_user_without_likes_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    data = get_post_feed_post_likes_data(
        request, post, False, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": None,
        "messages": None,
        "is_liked": False,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_unliked_post_with_one_like(
    user, user_permissions, post
):
    like_post(post, "DeletedUser")

    request = Mock(user=user, user_permissions=user_permissions)
    data = get_post_feed_post_likes_data(
        request, post, False, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 1,
        "messages": {
            "long": "DeletedUser likes this",
            "medium": "DeletedUser likes this",
            "short": "DeletedUser likes this",
        },
        "is_liked": False,
        "likes_url": "/likes-url/",
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_unliked_post_with_one_like_for_user_without_last_likes_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    like_post(post, "DeletedUser")

    data = get_post_feed_post_likes_data(
        request, post, False, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 1,
        "messages": {"count": "1 other likes this"},
        "is_liked": False,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_unliked_post_with_one_like_for_user_without_likes_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    like_post(post, "DeletedUser")

    data = get_post_feed_post_likes_data(
        request, post, False, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": None,
        "messages": None,
        "is_liked": False,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_liked_post_with_one_like(
    user, user_permissions, post
):
    like_post(post, user)

    request = Mock(user=user, user_permissions=user_permissions)
    data = get_post_feed_post_likes_data(
        request, post, True, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 1,
        "messages": None,
        "is_liked": True,
        "likes_url": "/likes-url/",
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_liked_post_with_one_like_for_user_without_last_likes_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    like_post(post, user)

    data = get_post_feed_post_likes_data(
        request, post, True, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 1,
        "messages": None,
        "is_liked": True,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_liked_post_with_one_like_for_user_without_likes_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    like_post(post, user)

    data = get_post_feed_post_likes_data(
        request, post, True, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": None,
        "messages": None,
        "is_liked": True,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_unliked_post_with_two_likes(
    user, user_permissions, post
):
    like_post(post, "DeletedUser")
    like_post(post, "OtherUser")

    request = Mock(user=user, user_permissions=user_permissions)
    data = get_post_feed_post_likes_data(
        request, post, False, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 2,
        "messages": {
            "long": "OtherUser and DeletedUser like this",
            "medium": "OtherUser and DeletedUser like this",
            "short": "OtherUser and DeletedUser like this",
        },
        "is_liked": False,
        "likes_url": "/likes-url/",
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_unliked_post_with_two_likes_for_user_without_last_likes_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    like_post(post, "DeletedUser")
    like_post(post, "OtherUser")

    data = get_post_feed_post_likes_data(
        request, post, False, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 2,
        "messages": {"count": "2 others like this"},
        "is_liked": False,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_unliked_post_with_two_likes_for_user_without_likes_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    like_post(post, "DeletedUser")
    like_post(post, "OtherUser")

    data = get_post_feed_post_likes_data(
        request, post, False, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": None,
        "messages": None,
        "is_liked": False,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_liked_post_with_two_likes(
    user, user_permissions, post
):
    like_post(post, "DeletedUser")
    like_post(post, user)

    request = Mock(user=user, user_permissions=user_permissions)
    data = get_post_feed_post_likes_data(
        request, post, True, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 2,
        "messages": {
            "long": "You and DeletedUser like this",
            "medium": "You and DeletedUser like this",
            "short": "You and DeletedUser like this",
        },
        "is_liked": True,
        "likes_url": "/likes-url/",
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_liked_post_with_two_likes_for_user_without_last_likes_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    like_post(post, "DeletedUser")
    like_post(post, user)

    data = get_post_feed_post_likes_data(
        request, post, True, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 2,
        "messages": {"count": "You and 1 other like this"},
        "is_liked": True,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_liked_post_with_two_likes_for_user_without_likes_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    like_post(post, "DeletedUser")
    like_post(post, user)

    data = get_post_feed_post_likes_data(
        request, post, True, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": None,
        "messages": None,
        "is_liked": True,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_unliked_post_with_fifty_likes(
    user, user_permissions, post
):
    for i in range(1, 51):
        like_post(post, f"User{i}")

    request = Mock(user=user, user_permissions=user_permissions)
    data = get_post_feed_post_likes_data(
        request, post, False, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 50,
        "messages": {
            "short": "User50, User49, User48, User47, User46 and 45 others like this",
            "medium": "User50, User49, User48, User47, User46, User45, User44, User43, User42, User41 and 40 others like this",
            "long": "User50, User49, User48, User47, User46, User45, User44, User43, User42, User41, User40, User39, User38, User37, User36, User35, User34, User33, User32, User31 and 30 others like this",
        },
        "is_liked": False,
        "likes_url": "/likes-url/",
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_unliked_post_with_fifty_likes_for_user_without_last_likes_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    for i in range(1, 51):
        like_post(post, f"User{i}")

    data = get_post_feed_post_likes_data(
        request, post, False, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 50,
        "messages": {"count": "50 others like this"},
        "is_liked": False,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_unliked_post_with_fifty_likes_for_user_without_likes_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    for i in range(1, 51):
        like_post(post, f"User{i}")

    data = get_post_feed_post_likes_data(
        request, post, False, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": None,
        "messages": None,
        "is_liked": False,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_liked_post_with_fifty_likes(
    user, user_permissions, post
):
    for i in range(1, 50):
        like_post(post, f"User{i}")

    like_post(post, user)

    request = Mock(user=user, user_permissions=user_permissions)
    data = get_post_feed_post_likes_data(
        request, post, True, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 50,
        "messages": {
            "short": "You, User49, User48, User47, User46 and 45 others like this",
            "medium": "You, User49, User48, User47, User46, User45, User44, User43, User42, User41 and 40 others like this",
            "long": "You, User49, User48, User47, User46, User45, User44, User43, User42, User41, User40, User39, User38, User37, User36, User35, User34, User33, User32, User31 and 30 others like this",
        },
        "is_liked": True,
        "likes_url": "/likes-url/",
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_liked_post_with_fifty_likes_for_user_without_last_likes_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    for i in range(1, 50):
        like_post(post, f"User{i}")

    like_post(post, user)

    data = get_post_feed_post_likes_data(
        request, post, True, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 50,
        "messages": {"count": "You and 49 others like this"},
        "is_liked": True,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_for_liked_post_with_fifty_likes_for_user_without_likes_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    for i in range(1, 50):
        like_post(post, f"User{i}")

    like_post(post, user)

    data = get_post_feed_post_likes_data(
        request, post, True, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": None,
        "messages": None,
        "is_liked": True,
        "likes_url": None,
        "like_url": "/like-url/",
        "unlike_url": "/unlike-url/",
    }


def test_get_post_feed_post_likes_data_hides_like_and_unlike_url_if_user_has_no_like_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_like_posts = False
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    data = get_post_feed_post_likes_data(
        request, post, False, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 0,
        "messages": None,
        "is_liked": False,
        "likes_url": None,
        "like_url": None,
        "unlike_url": None,
    }


def test_get_post_feed_post_likes_data_hides_like_and_unlike_url_for_liked_post_if_user_has_no_like_permission(
    user_permissions_factory, user, members_group, post
):
    members_group.can_like_posts = False
    members_group.save()

    user_permissions = user_permissions_factory(user)
    request = Mock(user=user, user_permissions=user_permissions)

    like_post(post, user)

    data = get_post_feed_post_likes_data(
        request, post, True, "/likes-url/", "/like-url/", "/unlike-url/"
    )

    assert data == {
        "likes": 1,
        "messages": None,
        "is_liked": True,
        "likes_url": "/likes-url/",
        "like_url": None,
        "unlike_url": None,
    }
