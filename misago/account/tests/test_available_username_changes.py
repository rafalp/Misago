from dataclasses import dataclass
from datetime import timedelta

from django.utils import timezone

from ..namechanges import get_available_username_changes


@dataclass
class Permissions:
    can_change_username: bool = False
    username_changes_limit: int = 0
    username_changes_expire: int = 0
    username_changes_span: int = 0


def test_get_available_username_changes_doesnt_allow_name_change_if_no_permission(user):
    options = get_available_username_changes(user, Permissions())

    assert not options.can_change_username
    assert options.unlimited is False
    assert options.changes_left == 0
    assert options.next_change is None


def test_get_available_username_changes_allows_unlimited_name_changes_without_wait(
    user,
):
    options = get_available_username_changes(
        user, Permissions(can_change_username=True)
    )

    assert options.can_change_username
    assert options.unlimited is True
    assert options.changes_left is None
    assert options.next_change is None


def test_get_available_username_changes_allows_unlimited_name_changes_without_wait_after_change(
    user,
):
    user.set_username("Bob", user)

    options = get_available_username_changes(
        user, Permissions(can_change_username=True)
    )

    assert options.can_change_username
    assert options.unlimited is True
    assert options.changes_left is None
    assert options.next_change is None


def test_get_available_username_changes_counts_user_name_changes_to_the_limit(user):
    user.set_username("Bob", user)

    options = get_available_username_changes(
        user,
        Permissions(
            can_change_username=True,
            username_changes_limit=2,
        ),
    )

    assert options.can_change_username
    assert options.unlimited is False
    assert options.changes_left is 1
    assert options.next_change is None


def test_get_available_username_changes_counts_recent_name_changes_to_the_limit(user):
    user.set_username("Bob", user)

    options = get_available_username_changes(
        user,
        Permissions(
            can_change_username=True,
            username_changes_limit=2,
            username_changes_expire=1,
        ),
    )

    assert options.can_change_username
    assert options.unlimited is False
    assert options.changes_left is 1
    assert options.next_change is None


def test_get_available_username_changes_doesnt_count_expired_name_changes_to_the_limit(
    user,
):
    change = user.set_username("Bob", user)
    change.changed_on -= timedelta(hours=2)
    change.save()

    options = get_available_username_changes(
        user,
        Permissions(
            can_change_username=True,
            username_changes_limit=2,
            username_changes_expire=1,
        ),
    )

    assert options.can_change_username
    assert options.unlimited is False
    assert options.changes_left is 2
    assert options.next_change is None


def test_get_available_username_changes_doesnt_count_user_name_changes_by_other_users_to_the_limit(
    admin, user
):
    user.set_username("Bob", admin)

    options = get_available_username_changes(
        user,
        Permissions(
            can_change_username=True,
            username_changes_limit=2,
        ),
    )

    assert options.can_change_username
    assert options.unlimited is False
    assert options.changes_left is 2
    assert options.next_change is None


def test_get_available_username_changes_includes_span_in_next_change(user):
    change = user.set_username("Bob", user)

    options = get_available_username_changes(
        user,
        Permissions(
            can_change_username=True,
            username_changes_span=1,
        ),
    )

    assert not options.can_change_username
    assert options.unlimited is True
    assert options.changes_left is None
    assert options.next_change > change.changed_on


def test_get_available_username_changes_includes_span_in_past_next_change(user):
    change = user.set_username("Bob", user)
    change.changed_on -= timedelta(hours=2)
    change.save()

    options = get_available_username_changes(
        user,
        Permissions(
            can_change_username=True,
            username_changes_span=1,
        ),
    )

    assert options.can_change_username
    assert options.unlimited is True
    assert options.changes_left is None
    assert options.next_change > change.changed_on
    assert options.next_change < timezone.now()


def test_get_available_username_changes_prevents_change_if_limit_is_met(
    user,
):
    user.set_username("Bob", user)

    options = get_available_username_changes(
        user,
        Permissions(
            can_change_username=True,
            username_changes_limit=1,
        ),
    )

    assert not options.can_change_username
    assert options.unlimited is False
    assert options.changes_left == 0
    assert options.next_change is None


def test_get_available_username_changes_prevents_change_if_limit_is_exceeded(
    user,
):
    user.set_username("Bob", user)
    user.set_username("Dan", user)

    options = get_available_username_changes(
        user,
        Permissions(
            can_change_username=True,
            username_changes_limit=1,
        ),
    )

    assert not options.can_change_username
    assert options.unlimited is False
    assert options.changes_left == 0
    assert options.next_change is None


def test_get_available_username_changes_next_change_is_expiration_if_greater(
    user,
):
    first_change = user.set_username("Bob", user)
    first_change.changed_on -= timedelta(hours=3)
    first_change.save()

    second_change = user.set_username("Dan", user)
    second_change.changed_on -= timedelta(hours=2)
    second_change.save()

    options = get_available_username_changes(
        user,
        Permissions(
            can_change_username=True,
            username_changes_limit=2,
            username_changes_expire=6,
            username_changes_span=1,
        ),
    )

    assert not options.can_change_username
    assert options.unlimited is False
    assert options.changes_left == 0
    assert options.next_change > first_change.changed_on
    assert options.next_change > second_change.changed_on
    assert options.next_change > timezone.now() + timedelta(hours=2)


def test_get_available_username_changes_next_change_is_span_if_greater(
    user,
):
    first_change = user.set_username("Bob", user)
    first_change.changed_on -= timedelta(hours=2)
    first_change.save()

    second_change = user.set_username("Dan", user)

    options = get_available_username_changes(
        user,
        Permissions(
            can_change_username=True,
            username_changes_limit=2,
            username_changes_expire=3,
            username_changes_span=5,
        ),
    )

    assert not options.can_change_username
    assert options.unlimited is False
    assert options.changes_left == 0
    assert options.next_change > second_change.changed_on
    assert options.next_change > timezone.now() + timedelta(hours=4)
