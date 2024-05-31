from dataclasses import dataclass
from datetime import datetime, timedelta

from django.utils import timezone


@dataclass
class AvailableUsernameChanges:
    unlimited: bool
    changes_left: int | None
    next_change: datetime | None

    @property
    def can_change_username(self) -> bool:
        if self.unlimited or self.changes_left > 0:
            return bool(self.next_change is None or self.next_change < timezone.now())

        return False


def get_available_username_changes(user, permissions) -> AvailableUsernameChanges:
    if not permissions.can_change_username:
        return AvailableUsernameChanges(
            unlimited=False,
            changes_left=0,
            next_change=None,
        )

    changes_left = get_username_changes_left(user, permissions)
    next_change = get_username_next_change(user, permissions, changes_left)

    return AvailableUsernameChanges(
        unlimited=permissions.username_changes_limit == 0,
        changes_left=changes_left,
        next_change=next_change,
    )


def get_username_changes_left(user, permissions) -> int | None:
    if permissions.username_changes_limit == 0:
        return None

    queryset = user.namechanges.filter(changed_by=user)

    if permissions.username_changes_expire:
        expired_cutoff = timezone.now() - timedelta(
            hours=permissions.username_changes_expire,
        )
        queryset = queryset.filter(changed_on__gt=expired_cutoff)

    return max((permissions.username_changes_limit - queryset.count(), 0))


def get_username_next_change(user, permissions, changes_left: int) -> datetime | None:
    if changes_left == 0:
        return get_username_next_change_if_out_of_changes(user, permissions)

    # User has either unlimited changes or some changes left
    if permissions.username_changes_span:
        return get_newest_change(user, permissions)

    return None


def get_username_next_change_if_out_of_changes(user, permissions) -> datetime | None:
    # Changes don't expire, no more changes will be possible for the user
    if not permissions.username_changes_expire:
        return None

    oldest_change = get_oldest_expiring_change(user, permissions)
    if oldest_change is None:
        return None

    # We'll be able to change username when oldest change expires
    if not permissions.username_changes_span:
        return oldest_change

    newest_change = get_newest_change(user, permissions)
    if newest_change is None:
        return None

    return max((oldest_change, newest_change))


def get_oldest_expiring_change(user, permissions) -> datetime | None:
    expired_cutoff = timezone.now() - timedelta(
        hours=permissions.username_changes_expire,
    )

    change = user.namechanges.filter(
        changed_by=user,
        changed_on__gt=expired_cutoff,
    ).first()

    if not change:
        return None

    return change.changed_on + timedelta(
        hours=permissions.username_changes_expire,
    )


def get_newest_change(user, permissions) -> datetime | None:
    change = user.namechanges.filter(changed_by=user).last()

    if not change:
        return None

    return change.changed_on + timedelta(
        hours=permissions.username_changes_span,
    )
