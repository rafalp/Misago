from ...permissions.models import Moderator
from ..threads import (
    get_category_threads_moderation_actions,
    get_threads_moderation_actions,
)


def test_get_threads_moderation_actions_returns_actions_for_global_moderator(
    user_permissions_factory, moderator
):
    user_permissions = user_permissions_factory(moderator)
    assert get_threads_moderation_actions(user_permissions)


def test_get_threads_moderation_actions_returns_actions_for_category_moderator(
    user_permissions_factory, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    user_permissions = user_permissions_factory(user)
    assert get_threads_moderation_actions(user_permissions)


def test_get_threads_moderation_actions_returns_empty_list_for_user(
    user_permissions_factory, user
):
    user_permissions = user_permissions_factory(user)
    assert not get_threads_moderation_actions(user_permissions)


def test_get_threads_moderation_actions_returns_empty_list_for_anonymous_user(
    user_permissions_factory, anonymous_user
):
    user_permissions = user_permissions_factory(anonymous_user)
    assert not get_threads_moderation_actions(user_permissions)


def test_get_category_threads_moderation_actions_returns_actions_for_global_moderator(
    user_permissions_factory, moderator, default_category
):
    user_permissions = user_permissions_factory(moderator)
    assert get_category_threads_moderation_actions(user_permissions, default_category)


def test_get_category_threads_moderation_actions_returns_actions_for_category_moderator(
    user_permissions_factory, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    user_permissions = user_permissions_factory(user)
    assert get_category_threads_moderation_actions(user_permissions, default_category)


def test_get_category_threads_moderation_actions_returns_empty_list_for_other_category_moderator(
    user_permissions_factory, user, default_category, sibling_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[sibling_category.id],
    )

    user_permissions = user_permissions_factory(user)
    assert not get_category_threads_moderation_actions(
        user_permissions, default_category
    )


def test_get_category_threads_moderation_actions_returns_empty_list_for_user(
    user_permissions_factory, user, default_category
):
    user_permissions = user_permissions_factory(user)
    assert not get_category_threads_moderation_actions(
        user_permissions, default_category
    )


def test_get_category_threads_moderation_actions_returns_empty_list_for_anonymous_user(
    user_permissions_factory, anonymous_user, default_category
):
    user_permissions = user_permissions_factory(anonymous_user)
    assert not get_category_threads_moderation_actions(
        user_permissions, default_category
    )
