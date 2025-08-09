import pytest
from django.core.exceptions import ValidationError

from ...permissions.proxy import UserPermissionsProxy
from ...users.bans import ban_user
from ..validators import validate_new_private_thread_member


def test_validate_new_private_thread_member_passes(user, other_user, cache_versions):
    validate_new_private_thread_member(
        UserPermissionsProxy(user, cache_versions),
        UserPermissionsProxy(other_user, cache_versions),
        cache_versions,
    )


def test_validate_new_private_thread_member_fails_for_banned_user(
    user, other_user, cache_versions
):
    ban_user(user)

    with pytest.raises(ValidationError) as exc_info:
        validate_new_private_thread_member(
            UserPermissionsProxy(user, cache_versions),
            UserPermissionsProxy(other_user, cache_versions),
            cache_versions,
        )

    assert exc_info.value.messages == ["This user is banned."]


def test_validate_new_private_thread_member_fails_for_user_without_private_threads_permission(
    user, other_user, members_group, cache_versions
):
    members_group.can_use_private_threads = False
    members_group.save()

    with pytest.raises(ValidationError) as exc_info:
        validate_new_private_thread_member(
            UserPermissionsProxy(user, cache_versions),
            UserPermissionsProxy(other_user, cache_versions),
            cache_versions,
        )

    assert exc_info.value.messages == ["This user can't use private threads."]


def test_validate_new_private_thread_member_fails_for_user_who_disabled_private_thread_invites(
    user, other_user, cache_versions
):
    user.limits_private_thread_invites_to = user.LIMIT_INVITES_TO_NOBODY
    user.save()

    with pytest.raises(ValidationError) as exc_info:
        validate_new_private_thread_member(
            UserPermissionsProxy(user, cache_versions),
            UserPermissionsProxy(other_user, cache_versions),
            cache_versions,
        )

    assert exc_info.value.messages == [
        "This user limits who can invite them to private threads."
    ]


def test_validate_new_private_thread_member_passes_moderator_for_user_who_disabled_private_thread_invites(
    user, moderator, cache_versions
):
    user.limits_private_thread_invites_to = user.LIMIT_INVITES_TO_NOBODY
    user.save()

    validate_new_private_thread_member(
        UserPermissionsProxy(user, cache_versions),
        UserPermissionsProxy(moderator, cache_versions),
        cache_versions,
    )


def test_validate_new_private_thread_member_fails_for_user_who_limits_private_thread_invites_to_followed(
    user, other_user, cache_versions
):
    user.limits_private_thread_invites_to = user.LIMIT_INVITES_TO_FOLLOWED
    user.save()

    with pytest.raises(ValidationError) as exc_info:
        validate_new_private_thread_member(
            UserPermissionsProxy(user, cache_versions),
            UserPermissionsProxy(other_user, cache_versions),
            cache_versions,
        )

    assert exc_info.value.messages == [
        "This user limits who can invite them to private threads."
    ]


def test_validate_new_private_thread_member_passes_followed_for_user_who_limits_private_thread_invites_to_followed(
    user, other_user, cache_versions
):
    user.follows.add(other_user)
    user.limits_private_thread_invites_to = user.LIMIT_INVITES_TO_FOLLOWED
    user.save()

    validate_new_private_thread_member(
        UserPermissionsProxy(user, cache_versions),
        UserPermissionsProxy(other_user, cache_versions),
        cache_versions,
    )


def test_validate_new_private_thread_member_passes_moderator_for_user_who_limits_private_thread_invites_to_followed(
    user, moderator, cache_versions
):
    user.limits_private_thread_invites_to = user.LIMIT_INVITES_TO_FOLLOWED
    user.save()

    validate_new_private_thread_member(
        UserPermissionsProxy(user, cache_versions),
        UserPermissionsProxy(moderator, cache_versions),
        cache_versions,
    )
