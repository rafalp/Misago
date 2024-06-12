from typing import Any


def if_true(permissions: dict[str, Any], permission: str, value: bool):
    if value is True:
        permissions[permission] = True


def if_false(permissions: dict[str, Any], permission: str, value: bool):
    if value is False:
        permissions[permission] = False


def if_zero_or_greater(permissions: dict[str, Any], permission: str, value: int):
    if value == 0 or value > permissions[permission]:
        permissions[permission] = value


def if_greater(permissions: dict[str, Any], permission: str, value: int):
    if value > permissions[permission]:
        permissions[permission] = value


def if_lesser(permissions: dict[str, Any], permission: str, value: int):
    if value < permissions[permission]:
        permissions[permission] = value
