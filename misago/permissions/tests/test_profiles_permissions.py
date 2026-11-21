import pytest
from django.core.exceptions import PermissionDenied

from ..enums import PermissionValue
from ..profiles import check_see_user_profile_permission


def test_check_see_user_profile_permission_passes_if_user_has_permission(
    user_permissions_factory, user, other_user
):
    permissions = user_permissions_factory(user)
    check_see_user_profile_permission(permissions, other_user)


def test_check_see_user_profile_permission_fails_if_user_has_no_permission(
    user_permissions_factory, user, other_user, members_group
):
    members_group.can_see_user_profiles = PermissionValue.NO
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_see_user_profile_permission(permissions, other_user)


def test_check_see_user_profile_permission_passes_user_without_permission_for_their_own_profile(
    user_permissions_factory, user, members_group
):
    members_group.can_see_user_profiles = PermissionValue.NO
    members_group.save()

    permissions = user_permissions_factory(user)

    check_see_user_profile_permission(permissions, user)


def test_check_see_user_profile_permission_passes_if_anonymous_user_has_permission(
    user_permissions_factory, anonymous_user, user
):
    permissions = user_permissions_factory(anonymous_user)
    check_see_user_profile_permission(permissions, user)


def test_check_see_user_profile_permission_fails_if_anonymous_user_has_no_permission(
    user_permissions_factory, anonymous_user, user, guests_group
):
    guests_group.can_see_user_profiles = PermissionValue.NO
    guests_group.save()

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_see_user_profile_permission(permissions, user)
