from typing import Any, List


def add_permission(perms: List[Any], value: Any):
    if value not in perms:
        perms.append(value)
