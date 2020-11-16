from datetime import timedelta

from ..namechanges import get_left_namechanges, get_next_available_namechange


def test_user_without_permission_to_change_name_has_no_changes_left(user):
    user_acl = {"name_changes_allowed": 0}
    assert get_left_namechanges(user, user_acl) == 0


def test_user_without_namechanges_has_all_changes_left(user):
    user_acl = {"name_changes_allowed": 3, "name_changes_expire": 0}
    assert get_left_namechanges(user, user_acl) == 3


def test_user_own_namechanges_are_subtracted_from_changes_left(user):
    user_acl = {"name_changes_allowed": 3, "name_changes_expire": 0}
    user.set_username("Changed")
    assert get_left_namechanges(user, user_acl) == 2


def test_user_own_recent_namechanges_subtract_from_changes_left(user):
    user_acl = {"name_changes_allowed": 3, "name_changes_expire": 5}
    user.set_username("Changed")
    assert get_left_namechanges(user, user_acl) == 2


def test_user_own_expired_namechanges_dont_subtract_from_changes_left(user):
    user_acl = {"name_changes_allowed": 3, "name_changes_expire": 5}

    username_change = user.set_username("Changed")
    username_change.changed_on -= timedelta(days=10)
    username_change.save()

    assert get_left_namechanges(user, user_acl) == 3


def test_user_namechanges_by_other_users_dont_subtract_from_changes_left(user):
    user_acl = {"name_changes_allowed": 3, "name_changes_expire": 0}

    username_change = user.set_username("Changed")
    username_change.changed_by = None
    username_change.save()

    assert get_left_namechanges(user, user_acl) == 3


def test_user_next_available_namechange_is_none_for_user_with_changes_left(user):
    user_acl = {"name_changes_allowed": 3, "name_changes_expire": 0}
    assert get_next_available_namechange(user, user_acl, 3) is None


def test_user_next_available_namechange_is_none_if_own_namechanges_dont_expire(user):
    user_acl = {"name_changes_allowed": 1, "name_changes_expire": 0}
    user.set_username("Changed")
    assert get_next_available_namechange(user, user_acl, 0) is None


def test_user_next_available_namechange_is_calculated_if_own_namechanges_expire(user):
    user_acl = {"name_changes_allowed": 1, "name_changes_expire": 1}

    username_change = user.set_username("Changed")
    next_change_on = get_next_available_namechange(user, user_acl, 0)

    assert next_change_on
    assert next_change_on == username_change.changed_on + timedelta(days=1)
