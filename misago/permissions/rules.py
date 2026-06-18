from typing import Any, Iterable

from .enums import CanHideOwnPostEdits, CanSeePostEdits, PermissionValue


def yes_no_never(permissions: Iterable[PermissionValue]) -> bool:
    if PermissionValue.NEVER in permissions:
        return False

    return bool(PermissionValue.YES in permissions)


def zero_or_greater(permissions: Iterable[int]) -> int:
    if 0 in permissions:
        return 0

    return max(permissions)


def can_see_post_edits(permissions: Iterable[CanSeePostEdits]) -> int:
    if CanSeePostEdits.NEVER in permissions:
        return CanSeePostEdits.NO
    return max(permissions)


def can_hide_own_post_edits(permissions: Iterable[CanHideOwnPostEdits]) -> int:
    if CanHideOwnPostEdits.NEVER in permissions:
        return CanHideOwnPostEdits.NO
    return max(permissions)
