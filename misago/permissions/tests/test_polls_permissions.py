import pytest
from django.core.exceptions import PermissionDenied

from ..polls import (
    check_close_thread_poll_permission,
    check_delete_thread_poll_permission,
    check_edit_thread_poll_permission,
    check_open_thread_poll_permission,
    check_start_poll_permission,
    check_start_thread_poll_permission,
    check_vote_in_thread_poll_permission,
)
from ..proxy import UserPermissionsProxy


def test_check_start_thread_poll_permission_passes_if_user_has_permission(
    user, user_permissions_factory, default_category, user_thread
):
    permissions = user_permissions_factory(user)
    check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_fails_if_user_is_anonymous(
    anonymous_user, user_permissions_factory, default_category, user_thread
):
    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_fails_if_user_has_no_permission(
    user, members_group, user_permissions_factory, default_category, user_thread
):
    members_group.can_start_polls = False
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_poll_permission_allows_user_to_start_polls(user, cache_versions):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_start_poll_permission(permissions)


def test_check_start_thread_poll_permission_fails_if_thread_has_poll(
    user, user_permissions_factory, default_category, user_thread, user_poll
):
    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_fails_if_user_is_not_thread_starter(
    user, user_permissions_factory, default_category, thread
):
    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_start_thread_poll_permission(permissions, default_category, thread)


def test_check_start_thread_poll_permission_passes_if_user_is_category_moderator(
    category_moderator_permissions, default_category, thread
):
    check_start_thread_poll_permission(
        category_moderator_permissions, default_category, thread
    )


def test_check_start_thread_poll_permission_passes_if_user_is_global_moderator(
    moderator, user_permissions_factory, default_category, user_thread
):
    permissions = user_permissions_factory(moderator)
    check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_fails_for_user_if_category_is_closed(
    user, user_permissions_factory, default_category, user_thread
):
    default_category.is_closed = True
    default_category.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_passes_for_category_moderator_if_category_is_closed(
    category_moderator_permissions, default_category, user_thread
):
    default_category.is_closed = True
    default_category.save()

    check_start_thread_poll_permission(
        category_moderator_permissions, default_category, user_thread
    )


def test_check_start_thread_poll_permission_passes_for_global_moderator_if_category_is_closed(
    moderator, user_permissions_factory, default_category, user_thread
):
    default_category.is_closed = True
    default_category.save()

    permissions = user_permissions_factory(moderator)
    check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_fails_for_user_if_thread_is_closed(
    user, user_permissions_factory, default_category, user_thread
):
    user_thread.is_closed = True
    user_thread.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_passes_for_category_moderator_if_thread_is_closed(
    category_moderator_permissions, default_category, user_thread
):
    user_thread.is_closed = True
    user_thread.save()

    check_start_thread_poll_permission(
        category_moderator_permissions, default_category, user_thread
    )


def test_check_start_thread_poll_permission_passes_for_global_moderator_if_thread_is_closed(
    moderator, user_permissions_factory, default_category, user_thread
):
    user_thread.is_closed = True
    user_thread.save()

    permissions = user_permissions_factory(moderator)
    check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_edit_thread_poll_permission_passes_if_user_has_permission(
    user, user_permissions_factory, default_category, user_thread, user_poll
):
    permissions = user_permissions_factory(user)
    check_edit_thread_poll_permission(
        permissions, default_category, user_thread, user_poll
    )


def test_check_edit_thread_poll_permission_fails_if_user_has_no_permission(
    user,
    user_permissions_factory,
    members_group,
    default_category,
    user_thread,
    user_poll,
):
    members_group.can_edit_own_polls = False
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_edit_thread_poll_permission(
            permissions, default_category, user_thread, user_poll
        )


def test_check_edit_thread_poll_permission_passes_category_moderator(
    category_moderator_permissions,
    members_group,
    default_category,
    user_thread,
    user_poll,
):
    members_group.can_edit_own_polls = False
    members_group.save()

    check_edit_thread_poll_permission(
        category_moderator_permissions, default_category, user_thread, user_poll
    )


def test_check_edit_thread_poll_permission_passes_global_moderator(
    moderator_permissions,
    moderators_group,
    default_category,
    user_thread,
    user_poll,
):
    moderators_group.can_edit_own_polls = False
    moderators_group.save()

    check_edit_thread_poll_permission(
        moderator_permissions, default_category, user_thread, user_poll
    )


def test_check_edit_thread_poll_permission_fails_if_user_is_anonymous(
    anonymous_user_permissions,
    default_category,
    user_thread,
    user_poll,
):
    with pytest.raises(PermissionDenied):
        check_edit_thread_poll_permission(
            anonymous_user_permissions, default_category, user_thread, user_poll
        )


def test_check_edit_thread_poll_permission_fails_if_user_is_not_thread_starter(
    user,
    user_permissions_factory,
    default_category,
    other_user_thread,
    poll_factory,
):
    poll = poll_factory(other_user_thread, starter=user)
    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_edit_thread_poll_permission(
            permissions, default_category, other_user_thread, poll
        )


def test_check_edit_thread_poll_permission_fails_if_user_is_not_poll_starter(
    user,
    other_user,
    user_permissions_factory,
    default_category,
    user_thread,
    poll_factory,
):
    poll = poll_factory(user_thread, starter=other_user)
    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_edit_thread_poll_permission(
            permissions, default_category, user_thread, poll
        )


def test_check_edit_thread_poll_permission_fails_if_category_is_closed(
    user_permissions,
    default_category,
    user_thread,
    user_poll,
):
    default_category.is_closed = True
    default_category.save()

    with pytest.raises(PermissionDenied):
        check_edit_thread_poll_permission(
            user_permissions, default_category, user_thread, user_poll
        )


def test_check_edit_thread_poll_permission_passes_if_category_is_closed_for_category_moderator(
    category_moderator_permissions,
    default_category,
    user_thread,
    user_poll,
):
    default_category.is_closed = True
    default_category.save()

    check_edit_thread_poll_permission(
        category_moderator_permissions, default_category, user_thread, user_poll
    )


def test_check_edit_thread_poll_permission_passes_if_category_is_closed_for_global_moderator(
    moderator_permissions,
    default_category,
    user_thread,
    user_poll,
):
    default_category.is_closed = True
    default_category.save()

    check_edit_thread_poll_permission(
        moderator_permissions, default_category, user_thread, user_poll
    )


def test_check_edit_thread_poll_permission_fails_if_thread_is_closed(
    user_permissions,
    default_category,
    user_thread,
    user_poll,
):
    user_thread.is_closed = True
    user_thread.save()

    with pytest.raises(PermissionDenied):
        check_edit_thread_poll_permission(
            user_permissions, default_category, user_thread, user_poll
        )


def test_check_edit_thread_poll_permission_passes_for_category_moderator_if_thread_is_closed(
    category_moderator_permissions,
    default_category,
    user_thread,
    user_poll,
):
    user_thread.is_closed = True
    user_thread.save()

    check_edit_thread_poll_permission(
        category_moderator_permissions, default_category, user_thread, user_poll
    )


def test_check_edit_thread_poll_permission_passes_for_global_moderator_if_thread_is_closed(
    moderator_permissions,
    default_category,
    user_thread,
    user_poll,
):
    user_thread.is_closed = True
    user_thread.save()

    check_edit_thread_poll_permission(
        moderator_permissions, default_category, user_thread, user_poll
    )


def test_check_edit_thread_poll_permission_fails_if_poll_has_ended(
    user_permissions,
    default_category,
    user_thread,
    ended_user_poll,
):
    with pytest.raises(PermissionDenied):
        check_edit_thread_poll_permission(
            user_permissions, default_category, user_thread, ended_user_poll
        )


def test_check_edit_thread_poll_permission_passes_for_category_moderator_if_poll_has_ended(
    category_moderator_permissions,
    default_category,
    user_thread,
    ended_user_poll,
):
    check_edit_thread_poll_permission(
        category_moderator_permissions, default_category, user_thread, ended_user_poll
    )


def test_check_edit_thread_poll_permission_passes_for_global_moderator_if_poll_has_ended(
    moderator_permissions,
    default_category,
    user_thread,
    ended_user_poll,
):
    check_edit_thread_poll_permission(
        moderator_permissions, default_category, user_thread, ended_user_poll
    )


def test_check_edit_thread_poll_permission_fails_if_poll_is_closed(
    user_permissions,
    default_category,
    user_thread,
    closed_user_poll,
):
    with pytest.raises(PermissionDenied):
        check_edit_thread_poll_permission(
            user_permissions, default_category, user_thread, closed_user_poll
        )


def test_check_edit_thread_poll_permission_passes_for_category_moderator_if_poll_is_closed(
    category_moderator_permissions,
    default_category,
    user_thread,
    closed_user_poll,
):
    check_edit_thread_poll_permission(
        category_moderator_permissions, default_category, user_thread, closed_user_poll
    )


def test_check_edit_thread_poll_permission_passes_for_global_moderator_if_poll_is_closed(
    moderator_permissions,
    default_category,
    user_thread,
    closed_user_poll,
):
    check_edit_thread_poll_permission(
        moderator_permissions, default_category, user_thread, closed_user_poll
    )


def test_check_edit_thread_poll_permission_fails_if_poll_edit_time_has_expired(
    user,
    user_permissions_factory,
    members_group,
    default_category,
    user_thread,
    poll_factory,
    day_seconds,
):
    poll = poll_factory(user_thread, starter=user, started_at=day_seconds * -2)

    members_group.own_polls_edit_time_limit = 60 * 24
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_edit_thread_poll_permission(
            permissions, default_category, user_thread, poll
        )


def test_check_edit_thread_poll_permission_passes_for_category_moderator_if_poll_edit_time_has_expired(
    category_moderator,
    user_permissions_factory,
    members_group,
    default_category,
    user_thread,
    poll_factory,
    day_seconds,
):
    poll = poll_factory(
        user_thread, starter=category_moderator, started_at=day_seconds * -2
    )

    members_group.own_polls_edit_time_limit = 60 * 24
    members_group.save()

    permissions = user_permissions_factory(category_moderator)

    check_edit_thread_poll_permission(permissions, default_category, user_thread, poll)


def test_check_edit_thread_poll_permission_passes_for_global_moderator_if_poll_edit_time_has_expired(
    moderator,
    user_permissions_factory,
    moderators_group,
    default_category,
    user_thread,
    poll_factory,
    day_seconds,
):
    poll = poll_factory(user_thread, starter=moderator, started_at=day_seconds * -2)

    moderators_group.own_polls_edit_time_limit = 60 * 24
    moderators_group.save()

    permissions = user_permissions_factory(moderator)

    check_edit_thread_poll_permission(permissions, default_category, user_thread, poll)


def test_check_close_thread_poll_permission_passes_if_user_has_permission(
    user,
    user_permissions_factory,
    members_group,
    default_category,
    user_thread,
    user_poll,
):
    members_group.can_close_own_polls = True
    members_group.save()

    permissions = user_permissions_factory(user)

    check_close_thread_poll_permission(
        permissions, default_category, user_thread, user_poll
    )


def test_check_close_thread_poll_permission_fails_if_user_has_no_permission(
    user,
    user_permissions_factory,
    members_group,
    default_category,
    user_thread,
    user_poll,
):
    members_group.can_close_own_polls = False
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_close_thread_poll_permission(
            permissions, default_category, user_thread, user_poll
        )


def test_check_close_thread_poll_permission_passes_category_moderator(
    category_moderator,
    user_permissions_factory,
    members_group,
    default_category,
    user_thread,
    user_poll,
):
    members_group.can_close_own_polls = False
    members_group.save()

    permissions = user_permissions_factory(category_moderator)

    check_close_thread_poll_permission(
        permissions, default_category, user_thread, user_poll
    )


def test_check_close_thread_poll_permission_passes_global_moderator(
    moderator,
    user_permissions_factory,
    moderators_group,
    default_category,
    user_thread,
    user_poll,
):
    moderators_group.can_close_own_polls = False
    moderators_group.save()

    permissions = user_permissions_factory(moderator)

    check_close_thread_poll_permission(
        permissions, default_category, user_thread, user_poll
    )


def test_check_close_thread_poll_permission_fails_if_user_is_anonymous(
    anonymous_user,
    user_permissions_factory,
    guests_group,
    default_category,
    thread,
    poll,
):
    guests_group.can_close_own_polls = True
    guests_group.save()

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_close_thread_poll_permission(permissions, default_category, thread, poll)


def test_check_close_thread_poll_permission_fails_if_user_is_not_thread_starter(
    user,
    user_permissions_factory,
    members_group,
    default_category,
    other_user_thread,
    poll_factory,
):
    members_group.can_close_own_polls = True
    members_group.save()

    poll = poll_factory(other_user_thread, starter=user)
    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_close_thread_poll_permission(
            permissions, default_category, other_user_thread, poll
        )


def test_check_close_thread_poll_permission_fails_if_user_is_not_poll_starter(
    user,
    other_user,
    user_permissions_factory,
    members_group,
    default_category,
    user_thread,
    poll_factory,
):
    members_group.can_close_own_polls = True
    members_group.save()

    poll = poll_factory(user_thread, starter=other_user)
    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_close_thread_poll_permission(
            permissions, default_category, user_thread, poll
        )


def test_check_close_thread_poll_permission_fails_if_category_is_closed(
    user,
    user_permissions_factory,
    members_group,
    default_category,
    user_thread,
    user_poll,
):
    default_category.is_closed = True
    default_category.save()

    members_group.can_close_own_polls = True
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_close_thread_poll_permission(
            permissions, default_category, user_thread, user_poll
        )


def test_check_close_thread_poll_permission_passes_for_category_moderator_if_category_is_closed(
    category_moderator,
    user_permissions_factory,
    members_group,
    default_category,
    user_thread,
    user_poll,
):
    default_category.is_closed = True
    default_category.save()

    members_group.can_close_own_polls = True
    members_group.save()

    permissions = user_permissions_factory(category_moderator)

    check_close_thread_poll_permission(
        permissions, default_category, user_thread, user_poll
    )


def test_check_close_thread_poll_permission_passes_for_global_moderator_if_category_is_closed(
    moderator,
    user_permissions_factory,
    moderators_group,
    default_category,
    user_thread,
    user_poll,
):
    default_category.is_closed = True
    default_category.save()

    moderators_group.can_close_own_polls = True
    moderators_group.save()

    permissions = user_permissions_factory(moderator)

    check_close_thread_poll_permission(
        permissions, default_category, user_thread, user_poll
    )


def test_check_close_thread_poll_permission_fails_if_thread_is_closed(
    user,
    user_permissions_factory,
    members_group,
    default_category,
    user_thread,
    user_poll,
):
    user_thread.is_closed = True
    user_thread.save()

    members_group.can_close_own_polls = True
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_close_thread_poll_permission(
            permissions, default_category, user_thread, user_poll
        )


def test_check_close_thread_poll_permission_passes_for_category_moderator_if_thread_is_closed(
    category_moderator,
    user_permissions_factory,
    members_group,
    default_category,
    user_thread,
    user_poll,
):
    user_thread.is_closed = True
    user_thread.save()

    members_group.can_close_own_polls = True
    members_group.save()

    permissions = user_permissions_factory(category_moderator)

    check_close_thread_poll_permission(
        permissions, default_category, user_thread, user_poll
    )


def test_check_close_thread_poll_permission_passes_for_global_moderator_if_thread_is_closed(
    moderator,
    user_permissions_factory,
    moderators_group,
    default_category,
    user_thread,
    user_poll,
):
    user_thread.is_closed = True
    user_thread.save()

    moderators_group.can_close_own_polls = True
    moderators_group.save()

    permissions = user_permissions_factory(moderator)

    check_close_thread_poll_permission(
        permissions, default_category, user_thread, user_poll
    )


def test_check_close_thread_poll_permission_fails_if_poll_close_time_has_expired(
    user,
    user_permissions_factory,
    members_group,
    default_category,
    user_thread,
    poll_factory,
    day_seconds,
):
    poll = poll_factory(user_thread, starter=user, started_at=day_seconds * -2)

    members_group.can_close_own_polls = True
    members_group.own_polls_close_time_limit = 60 * 24
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_close_thread_poll_permission(
            permissions, default_category, user_thread, poll
        )


def test_check_close_thread_poll_permission_passes_for_category_moderator_if_poll_close_time_has_expired(
    category_moderator,
    user_permissions_factory,
    members_group,
    default_category,
    user_thread,
    poll_factory,
    day_seconds,
):
    poll = poll_factory(
        user_thread, starter=category_moderator, started_at=day_seconds * -2
    )

    members_group.can_close_own_polls = True
    members_group.own_polls_close_time_limit = 60 * 24
    members_group.save()

    permissions = user_permissions_factory(category_moderator)

    check_close_thread_poll_permission(permissions, default_category, user_thread, poll)


def test_check_close_thread_poll_permission_passes_for_global_moderator_if_poll_close_time_has_expired(
    moderator,
    user_permissions_factory,
    moderators_group,
    default_category,
    user_thread,
    poll_factory,
    day_seconds,
):
    poll = poll_factory(user_thread, starter=moderator, started_at=day_seconds * -2)

    moderators_group.can_close_own_polls = True
    moderators_group.own_polls_close_time_limit = 60 * 24
    moderators_group.save()

    permissions = user_permissions_factory(moderator)

    check_close_thread_poll_permission(permissions, default_category, user_thread, poll)


def test_check_open_thread_poll_permission_passes_category_moderator(
    category_moderator,
    user_permissions_factory,
    default_category,
    user_thread,
    user_poll,
):
    permissions = user_permissions_factory(category_moderator)

    check_open_thread_poll_permission(
        permissions, default_category, user_thread, user_poll
    )


def test_check_open_thread_poll_permission_passes_global_moderator(
    moderator,
    user_permissions_factory,
    default_category,
    user_thread,
    user_poll,
):
    permissions = user_permissions_factory(moderator)

    check_open_thread_poll_permission(
        permissions, default_category, user_thread, user_poll
    )


def test_check_open_thread_poll_permission_fails_if_user_is_anonymous(
    anonymous_user,
    user_permissions_factory,
    default_category,
    thread,
    poll,
):
    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_open_thread_poll_permission(permissions, default_category, thread, poll)


def test_check_open_thread_poll_permission_fails_if_user_is_not_moderator(
    user,
    user_permissions_factory,
    default_category,
    other_user_thread,
    poll_factory,
):
    poll = poll_factory(other_user_thread, starter=user)
    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_open_thread_poll_permission(
            permissions, default_category, other_user_thread, poll
        )


def test_check_delete_thread_poll_permission_passes_category_moderator(
    category_moderator,
    user_permissions_factory,
    default_category,
    user_thread,
    user_poll,
):
    permissions = user_permissions_factory(category_moderator)

    check_delete_thread_poll_permission(
        permissions, default_category, user_thread, user_poll
    )


def test_check_delete_thread_poll_permission_passes_global_moderator(
    moderator,
    user_permissions_factory,
    default_category,
    user_thread,
    user_poll,
):
    permissions = user_permissions_factory(moderator)

    check_delete_thread_poll_permission(
        permissions, default_category, user_thread, user_poll
    )


def test_check_delete_thread_poll_permission_fails_if_user_is_anonymous(
    anonymous_user,
    user_permissions_factory,
    default_category,
    thread,
    poll,
):
    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_delete_thread_poll_permission(permissions, default_category, thread, poll)


def test_check_delete_thread_poll_permission_fails_if_user_is_not_moderator(
    user,
    user_permissions_factory,
    default_category,
    other_user_thread,
    poll_factory,
):
    poll = poll_factory(other_user_thread, starter=user)
    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_delete_thread_poll_permission(
            permissions, default_category, other_user_thread, poll
        )


def test_check_vote_in_thread_poll_permission_passes_if_user_has_permission(
    user_permissions,
    default_category,
    user_thread,
    user_poll,
):
    check_vote_in_thread_poll_permission(
        user_permissions, default_category, user_thread, user_poll
    )


def test_check_vote_in_thread_poll_permission_fails_if_user_is_anonymous(
    anonymous_user_permissions,
    default_category,
    thread,
    poll,
):
    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            anonymous_user_permissions, default_category, thread, poll
        )


def test_check_vote_in_thread_poll_permission_fails_if_user_has_no_permission(
    user,
    user_permissions_factory,
    members_group,
    default_category,
    thread,
    poll,
):
    members_group.can_vote_in_polls = False
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            permissions, default_category, thread, poll
        )


def test_check_vote_in_thread_poll_permission_fails_if_category_moderator_has_no_permission(
    category_moderator,
    user_permissions_factory,
    members_group,
    default_category,
    thread,
    poll,
):
    members_group.can_vote_in_polls = False
    members_group.save()

    permissions = user_permissions_factory(category_moderator)

    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            permissions, default_category, thread, poll
        )


def test_check_vote_in_thread_poll_permission_fails_if_global_moderator_has_no_permission(
    moderator,
    user_permissions_factory,
    moderators_group,
    default_category,
    thread,
    poll,
):
    moderators_group.can_vote_in_polls = False
    moderators_group.save()

    permissions = user_permissions_factory(moderator)

    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            permissions, default_category, thread, poll
        )


def test_check_vote_in_thread_poll_permission_fails_if_category_is_closed(
    user_permissions,
    default_category,
    thread,
    poll,
):
    default_category.is_closed = True
    default_category.save()

    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            user_permissions, default_category, thread, poll
        )


def test_check_vote_in_thread_poll_permission_fails_for_category_moderator_if_category_is_closed(
    category_moderator_permissions,
    default_category,
    thread,
    poll,
):
    default_category.is_closed = True
    default_category.save()

    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            category_moderator_permissions, default_category, thread, poll
        )


def test_check_vote_in_thread_poll_permission_fails_for_global_moderator_if_category_is_closed(
    moderator_permissions,
    default_category,
    thread,
    poll,
):
    default_category.is_closed = True
    default_category.save()

    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            moderator_permissions, default_category, thread, poll
        )


def test_check_vote_in_thread_poll_permission_fails_if_thread_is_closed(
    user_permissions,
    default_category,
    thread,
    poll,
):
    thread.is_closed = True
    thread.save()

    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            user_permissions, default_category, thread, poll
        )


def test_check_vote_in_thread_poll_permission_fails_for_category_moderator_if_thread_is_closed(
    category_moderator_permissions,
    default_category,
    thread,
    poll,
):
    thread.is_closed = True
    thread.save()

    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            category_moderator_permissions, default_category, thread, poll
        )


def test_check_vote_in_thread_poll_permission_fails_for_global_moderator_if_thread_is_closed(
    moderator_permissions,
    default_category,
    thread,
    poll,
):
    thread.is_closed = True
    thread.save()

    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            moderator_permissions, default_category, thread, poll
        )


def test_check_vote_in_thread_poll_permission_fails_if_poll_has_ended(
    user_permissions,
    default_category,
    thread,
    ended_poll,
):
    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            user_permissions, default_category, thread, ended_poll
        )


def test_check_vote_in_thread_poll_permission_fails_for_category_moderator_if_poll_has_ended(
    category_moderator_permissions,
    default_category,
    thread,
    ended_poll,
):
    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            category_moderator_permissions, default_category, thread, ended_poll
        )


def test_check_vote_in_thread_poll_permission_fails_for_global_moderator_if_poll_has_ended(
    moderator_permissions,
    default_category,
    thread,
    ended_poll,
):
    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            moderator_permissions, default_category, thread, ended_poll
        )


def test_check_vote_in_thread_poll_permission_fails_if_poll_is_closed(
    user_permissions,
    default_category,
    thread,
    closed_poll,
):
    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            user_permissions, default_category, thread, closed_poll
        )


def test_check_vote_in_thread_poll_permission_fails_for_category_moderator_if_poll_is_closed(
    category_moderator_permissions,
    default_category,
    thread,
    closed_poll,
):
    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            category_moderator_permissions, default_category, thread, closed_poll
        )


def test_check_vote_in_thread_poll_permission_fails_for_global_moderator_if_poll_is_closed(
    moderator_permissions,
    default_category,
    thread,
    closed_poll,
):
    with pytest.raises(PermissionDenied):
        check_vote_in_thread_poll_permission(
            moderator_permissions, default_category, thread, closed_poll
        )
