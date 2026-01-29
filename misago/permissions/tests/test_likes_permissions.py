import pytest
from django.core.exceptions import PermissionDenied

from ..enums import CanSeePostLikes
from ..likes import (
    can_see_post_likes_count,
    check_like_post_permission,
    check_see_post_likes_permission,
    check_unlike_post_permission,
)


def test_check_like_post_permission_passes_if_user_has_permission(
    user, user_permissions_factory, default_category, thread, post
):
    permissions = user_permissions_factory(user)
    check_like_post_permission(permissions, default_category, thread, post)


def test_check_like_post_permission_fails_if_user_is_anonymous(
    anonymous_user, user_permissions_factory, default_category, thread, post
):
    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_like_post_permission(permissions, default_category, thread, post)


def test_check_like_post_permission_fails_if_user_has_no_permission(
    user, members_group, user_permissions_factory, default_category, thread, post
):
    members_group.can_like_posts = False
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_like_post_permission(permissions, default_category, thread, post)


def test_check_unlike_post_permission_passes_if_user_has_permission(
    user, user_permissions_factory, default_category, thread, post
):
    permissions = user_permissions_factory(user)
    check_unlike_post_permission(permissions, default_category, thread, post)


def test_check_unlike_post_permission_fails_if_user_is_anonymous(
    anonymous_user, user_permissions_factory, default_category, thread, post
):
    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_unlike_post_permission(permissions, default_category, thread, post)


def test_check_unlike_post_permission_fails_if_user_has_no_permission(
    user, members_group, user_permissions_factory, default_category, thread, post
):
    members_group.can_like_posts = False
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_unlike_post_permission(permissions, default_category, thread, post)


def test_can_see_post_likes_count_returns_true_if_user_has_count_permission_to_own_posts(
    user, members_group, user_permissions_factory, default_category, thread, user_reply
):
    members_group.can_see_own_post_likes = CanSeePostLikes.COUNT
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)
    assert can_see_post_likes_count(permissions, default_category, thread, user_reply)


def test_can_see_post_likes_count_returns_true_if_user_has_permission_to_own_posts(
    user, members_group, user_permissions_factory, default_category, thread, user_reply
):
    members_group.can_see_own_post_likes = CanSeePostLikes.USERS
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)
    assert can_see_post_likes_count(permissions, default_category, thread, user_reply)


def test_can_see_post_likes_count_returns_false_if_user_has_no_permission_to_own_posts(
    user, members_group, user_permissions_factory, default_category, thread, user_reply
):
    members_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    members_group.can_see_others_post_likes = CanSeePostLikes.USERS
    members_group.save()

    permissions = user_permissions_factory(user)
    assert not can_see_post_likes_count(
        permissions, default_category, thread, user_reply
    )


def test_can_see_post_likes_count_returns_true_if_user_has_count_permission_to_other_users_posts(
    user,
    members_group,
    user_permissions_factory,
    default_category,
    thread,
    other_user_reply,
):
    members_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    members_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    permissions = user_permissions_factory(user)
    assert can_see_post_likes_count(
        permissions, default_category, thread, other_user_reply
    )


def test_can_see_post_likes_count_returns_true_if_user_has_permission_to_other_users_posts(
    user,
    members_group,
    user_permissions_factory,
    default_category,
    thread,
    other_user_reply,
):
    members_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    members_group.can_see_others_post_likes = CanSeePostLikes.USERS
    members_group.save()

    permissions = user_permissions_factory(user)
    assert can_see_post_likes_count(
        permissions, default_category, thread, other_user_reply
    )


def test_can_see_post_likes_count_returns_false_if_user_has_no_permission_to_other_users_posts(
    user,
    members_group,
    user_permissions_factory,
    default_category,
    thread,
    other_user_reply,
):
    members_group.can_see_own_post_likes = CanSeePostLikes.USERS
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)
    assert not can_see_post_likes_count(
        permissions, default_category, thread, other_user_reply
    )


def test_can_see_post_likes_count_returns_true_if_user_has_count_permission_to_deleted_users_posts(
    user, members_group, user_permissions_factory, default_category, thread, post
):
    members_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    members_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    permissions = user_permissions_factory(user)
    assert can_see_post_likes_count(permissions, default_category, thread, post)


def test_can_see_post_likes_count_returns_true_if_user_has_permission_to_deleted_users_posts(
    user, members_group, user_permissions_factory, default_category, thread, post
):
    members_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    members_group.can_see_others_post_likes = CanSeePostLikes.USERS
    members_group.save()

    permissions = user_permissions_factory(user)
    assert can_see_post_likes_count(permissions, default_category, thread, post)


def test_can_see_post_likes_count_returns_false_if_user_has_no_permission_to_deled_users_posts(
    user, members_group, user_permissions_factory, default_category, thread, post
):
    members_group.can_see_own_post_likes = CanSeePostLikes.USERS
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)
    assert not can_see_post_likes_count(permissions, default_category, thread, post)


def test_can_see_post_likes_count_returns_true_if_anonymous_user_has_count_permission_to_other_users_posts(
    anonymous_user,
    guests_group,
    user_permissions_factory,
    default_category,
    thread,
    other_user_reply,
):
    guests_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    guests_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    guests_group.save()

    permissions = user_permissions_factory(anonymous_user)
    assert can_see_post_likes_count(
        permissions, default_category, thread, other_user_reply
    )


def test_can_see_post_likes_count_returns_true_if_anonymous_user_has_permission_to_other_users_posts(
    anonymous_user,
    guests_group,
    user_permissions_factory,
    default_category,
    thread,
    other_user_reply,
):
    guests_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    guests_group.can_see_others_post_likes = CanSeePostLikes.USERS
    guests_group.save()

    permissions = user_permissions_factory(anonymous_user)
    assert can_see_post_likes_count(
        permissions, default_category, thread, other_user_reply
    )


def test_can_see_post_likes_count_returns_false_if_anonymous_user_has_no_permission_to_other_users_posts(
    anonymous_user,
    guests_group,
    user_permissions_factory,
    default_category,
    thread,
    other_user_reply,
):
    guests_group.can_see_own_post_likes = CanSeePostLikes.USERS
    guests_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    guests_group.save()

    permissions = user_permissions_factory(anonymous_user)
    assert not can_see_post_likes_count(
        permissions, default_category, thread, other_user_reply
    )


def test_can_see_post_likes_count_returns_true_if_anonymous_user_has_count_permission_to_deleted_users_posts(
    anonymous_user,
    guests_group,
    user_permissions_factory,
    default_category,
    thread,
    post,
):
    guests_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    guests_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    guests_group.save()

    permissions = user_permissions_factory(anonymous_user)
    assert can_see_post_likes_count(permissions, default_category, thread, post)


def test_can_see_post_likes_count_returns_true_if_anonymous_user_has_permission_to_deleted_users_posts(
    anonymous_user,
    guests_group,
    user_permissions_factory,
    default_category,
    thread,
    post,
):
    guests_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    guests_group.can_see_others_post_likes = CanSeePostLikes.USERS
    guests_group.save()

    permissions = user_permissions_factory(anonymous_user)
    assert can_see_post_likes_count(permissions, default_category, thread, post)


def test_can_see_post_likes_count_returns_false_if_anonymous_user_has_no_permission_to_deled_users_posts(
    anonymous_user,
    guests_group,
    user_permissions_factory,
    default_category,
    thread,
    post,
):
    guests_group.can_see_own_post_likes = CanSeePostLikes.USERS
    guests_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    guests_group.save()

    permissions = user_permissions_factory(anonymous_user)
    assert not can_see_post_likes_count(permissions, default_category, thread, post)


def test_check_see_post_likes_permission_passes_if_user_has_permission_to_own_posts(
    user, members_group, user_permissions_factory, default_category, thread, user_reply
):
    members_group.can_see_own_post_likes = CanSeePostLikes.USERS
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)
    check_see_post_likes_permission(permissions, default_category, thread, user_reply)


def test_check_see_post_likes_permission_fails_if_user_has_count_permission_to_own_posts(
    user, members_group, user_permissions_factory, default_category, thread, user_reply
):
    members_group.can_see_own_post_likes = CanSeePostLikes.COUNT
    members_group.can_see_others_post_likes = CanSeePostLikes.USERS
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_see_post_likes_permission(
            permissions, default_category, thread, user_reply
        )


def test_check_see_post_likes_permission_fails_if_user_has_no_permission_to_own_posts(
    user, members_group, user_permissions_factory, default_category, thread, user_reply
):
    members_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    members_group.can_see_others_post_likes = CanSeePostLikes.USERS
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_see_post_likes_permission(
            permissions, default_category, thread, user_reply
        )


def test_check_see_post_likes_permission_passes_if_user_has_permission_to_other_users_posts(
    user,
    members_group,
    user_permissions_factory,
    default_category,
    thread,
    other_user_reply,
):
    members_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    members_group.can_see_others_post_likes = CanSeePostLikes.USERS
    members_group.save()

    permissions = user_permissions_factory(user)
    check_see_post_likes_permission(
        permissions, default_category, thread, other_user_reply
    )


def test_check_see_post_likes_permission_passes_if_user_has_permission_to_deleted_users_posts(
    user,
    members_group,
    user_permissions_factory,
    default_category,
    thread,
    post,
):
    members_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    members_group.can_see_others_post_likes = CanSeePostLikes.USERS
    members_group.save()

    permissions = user_permissions_factory(user)
    check_see_post_likes_permission(permissions, default_category, thread, post)


def test_check_see_post_likes_permission_fails_if_user_has_count_permission_to_other_users_posts(
    user,
    members_group,
    user_permissions_factory,
    default_category,
    thread,
    other_user_reply,
):
    members_group.can_see_own_post_likes = CanSeePostLikes.USERS
    members_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_see_post_likes_permission(
            permissions, default_category, thread, other_user_reply
        )


def test_check_see_post_likes_permission_fails_if_user_has_count_permission_to_deleted_users_posts(
    user,
    members_group,
    user_permissions_factory,
    default_category,
    thread,
    post,
):
    members_group.can_see_own_post_likes = CanSeePostLikes.USERS
    members_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_see_post_likes_permission(permissions, default_category, thread, post)


def test_check_see_post_likes_permission_fails_if_user_has_no_permission_to_other_users_posts(
    user,
    members_group,
    user_permissions_factory,
    default_category,
    thread,
    other_user_reply,
):
    members_group.can_see_own_post_likes = CanSeePostLikes.USERS
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_see_post_likes_permission(
            permissions, default_category, thread, other_user_reply
        )


def test_check_see_post_likes_permission_fails_if_user_has_no_permission_to_deleted_users_posts(
    user,
    members_group,
    user_permissions_factory,
    default_category,
    thread,
    post,
):
    members_group.can_see_own_post_likes = CanSeePostLikes.USERS
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_see_post_likes_permission(permissions, default_category, thread, post)


def test_check_see_post_likes_permission_passes_if_anonymous_user_has_permission_to_other_users_posts(
    anonymous_user,
    guests_group,
    user_permissions_factory,
    default_category,
    thread,
    other_user_reply,
):
    guests_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    guests_group.can_see_others_post_likes = CanSeePostLikes.USERS
    guests_group.save()

    permissions = user_permissions_factory(anonymous_user)
    check_see_post_likes_permission(
        permissions, default_category, thread, other_user_reply
    )


def test_check_see_post_likes_permission_passes_if_anonymous_user_has_permission_to_deleted_users_posts(
    anonymous_user,
    guests_group,
    user_permissions_factory,
    default_category,
    thread,
    post,
):
    guests_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    guests_group.can_see_others_post_likes = CanSeePostLikes.USERS
    guests_group.save()

    permissions = user_permissions_factory(anonymous_user)
    check_see_post_likes_permission(permissions, default_category, thread, post)


def test_check_see_post_likes_permission_fails_if_anonymous_user_has_count_permission_to_other_users_posts(
    anonymous_user,
    guests_group,
    user_permissions_factory,
    default_category,
    thread,
    other_user_reply,
):
    guests_group.can_see_own_post_likes = CanSeePostLikes.USERS
    guests_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    guests_group.save()

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_see_post_likes_permission(
            permissions, default_category, thread, other_user_reply
        )


def test_check_see_post_likes_permission_fails_if_anonymous_user_has_count_permission_to_deleted_users_posts(
    anonymous_user,
    guests_group,
    user_permissions_factory,
    default_category,
    thread,
    post,
):
    guests_group.can_see_own_post_likes = CanSeePostLikes.USERS
    guests_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    guests_group.save()

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_see_post_likes_permission(permissions, default_category, thread, post)


def test_check_see_post_likes_permission_fails_if_anonymous_user_has_no_permission_to_other_users_posts(
    anonymous_user,
    guests_group,
    user_permissions_factory,
    default_category,
    thread,
    other_user_reply,
):
    guests_group.can_see_own_post_likes = CanSeePostLikes.USERS
    guests_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    guests_group.save()

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_see_post_likes_permission(
            permissions, default_category, thread, other_user_reply
        )


def test_check_see_post_likes_permission_fails_if_anonymous_user_has_no_permission_to_deleted_users_posts(
    anonymous_user,
    guests_group,
    user_permissions_factory,
    default_category,
    thread,
    post,
):
    guests_group.can_see_own_post_likes = CanSeePostLikes.USERS
    guests_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    guests_group.save()

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_see_post_likes_permission(permissions, default_category, thread, post)
