from typing import Any, List


def add_permission(list: List[Any], value: Any):
    if value not in list:
        list.append(value)
