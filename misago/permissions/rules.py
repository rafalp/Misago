from typing import Any, Iterable

from .enums import PermissionValue


def yes_no_never(permissions: Iterable[PermissionValue]) -> bool:
    if PermissionValue.NEVER in permissions:
        return False

    return bool(PermissionValue.YES in permissions)


def zero_or_greater(permissions: Iterable[int]) -> int:
    if 0 in permissions:
        return 0

    return max(permissions)
