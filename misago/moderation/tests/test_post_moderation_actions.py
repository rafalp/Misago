from ...permissions.models import Moderator
from ..post import (
    get_private_thread_post_moderation_actions,
    get_thread_post_moderation_actions,
)


def test_get_thread_post_moderation_actions_returns_actions_for_global_moderator(
    user_permissions_factory, moderator, post
):
    user_permissions = user_permissions_factory(moderator)
    assert get_thread_post_moderation_actions(user_permissions, post)


def test_get_thread_post_moderation_actions_returns_actions_for_category_moderator(
    user_permissions_factory, user, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    user_permissions = user_permissions_factory(user)
    assert get_thread_post_moderation_actions(user_permissions, post)


def test_get_thread_post_moderation_actions_returns_empty_list_for_other_category_moderator(
    user_permissions_factory, user, post, sibling_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[sibling_category.id],
    )

    user_permissions = user_permissions_factory(user)
    assert not get_thread_post_moderation_actions(user_permissions, post)


def test_get_thread_post_moderation_actions_returns_empty_list_for_user(
    user_permissions_factory, user, post
):
    user_permissions = user_permissions_factory(user)
    assert not get_thread_post_moderation_actions(user_permissions, post)


def test_get_thread_post_moderation_actions_returns_empty_list_for_anonymous_user(
    user_permissions_factory, anonymous_user, post
):
    user_permissions = user_permissions_factory(anonymous_user)
    assert not get_thread_post_moderation_actions(user_permissions, post)


def test_get_private_thread_post_moderation_actions_returns_actions_for_global_moderator(
    user_permissions_factory, moderator, post
):
    user_permissions = user_permissions_factory(moderator)
    assert get_private_thread_post_moderation_actions(user_permissions, post)


def test_get_private_thread_post_moderation_actions_returns_actions_for_private_threads_moderator(
    user_permissions_factory, user, post
):
    Moderator.objects.create(user=user, is_global=False, private_threads=True)

    user_permissions = user_permissions_factory(user)
    assert get_private_thread_post_moderation_actions(user_permissions, post)


def test_get_private_thread_post_moderation_actions_returns_empty_list_for_category_moderator(
    user_permissions_factory, user, post, sibling_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[sibling_category.id],
    )

    user_permissions = user_permissions_factory(user)
    assert not get_private_thread_post_moderation_actions(user_permissions, post)


def test_get_private_thread_post_moderation_actions_returns_empty_list_for_user(
    user_permissions_factory, user, post
):
    user_permissions = user_permissions_factory(user)
    assert not get_private_thread_post_moderation_actions(user_permissions, post)


def test_get_private_thread_post_moderation_actions_returns_empty_list_for_anonymous_user(
    user_permissions_factory, anonymous_user, post
):
    user_permissions = user_permissions_factory(anonymous_user)
    assert not get_private_thread_post_moderation_actions(user_permissions, post)
