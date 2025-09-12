import pytest
from django.core.exceptions import ValidationError

from ...permissions.proxy import UserPermissionsProxy
from ...users.bans import ban_user
from ...users.enums import UserNewPrivateThreadsPreference
from ..validators import validate_new_private_thread_owner


def test_validate_new_private_thread_owner_passes(user, other_user, cache_versions):
    validate_new_private_thread_owner(
        UserPermissionsProxy(user, cache_versions),
        UserPermissionsProxy(other_user, cache_versions),
        cache_versions,
    )


def test_validate_new_private_thread_owner_fails_for_banned_user(
    user, other_user, cache_versions
):
    ban_user(user)

    with pytest.raises(ValidationError) as exc_info:
        validate_new_private_thread_owner(
            UserPermissionsProxy(user, cache_versions),
            UserPermissionsProxy(other_user, cache_versions),
            cache_versions,
        )

    assert exc_info.value.messages == ["This user is banned."]


def test_validate_new_private_thread_owner_fails_for_user_without_private_threads_permission(
    user, other_user, members_group, cache_versions
):
    members_group.can_use_private_threads = False
    members_group.save()

    with pytest.raises(ValidationError) as exc_info:
        validate_new_private_thread_owner(
            UserPermissionsProxy(user, cache_versions),
            UserPermissionsProxy(other_user, cache_versions),
            cache_versions,
        )

    assert exc_info.value.messages == ["This user can't use private threads."]


def test_validate_new_private_thread_owner_fails_for_user_without_start_private_threads_permission(
    user, other_user, members_group, cache_versions
):
    members_group.can_start_private_threads = False
    members_group.save()

    with pytest.raises(ValidationError) as exc_info:
        validate_new_private_thread_owner(
            UserPermissionsProxy(user, cache_versions),
            UserPermissionsProxy(other_user, cache_versions),
            cache_versions,
        )

    assert exc_info.value.messages == ["This user can't own private threads."]
