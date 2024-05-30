from ..operations import (
    if_false,
    if_greater,
    if_lesser,
    if_true,
    if_zero_or_greater,
)


def test_if_true_keeps_permission_false_if_value_is_false():
    permissions = {"permission": False}
    if_true(permissions, "permission", False)
    assert permissions == {"permission": False}


def test_if_true_changes_permission_to_true_if_value_is_true():
    permissions = {"permission": False}
    if_true(permissions, "permission", True)
    assert permissions == {"permission": True}


def test_if_false_keeps_permission_true_if_value_is_true():
    permissions = {"permission": True}
    if_false(permissions, "permission", True)
    assert permissions == {"permission": True}


def test_if_false_changes_permission_to_false_if_value_is_false():
    permissions = {"permission": True}
    if_false(permissions, "permission", False)
    assert permissions == {"permission": False}


def test_if_greater_keeps_permission_low_if_value_is_lesser():
    permissions = {"permission": 5}
    if_greater(permissions, "permission", 4)
    assert permissions == {"permission": 5}


def test_if_greater_changes_permission_if_value_is_greater():
    permissions = {"permission": 5}
    if_greater(permissions, "permission", 6)
    assert permissions == {"permission": 6}


def test_if_lesser_keeps_permission_high_if_value_is_greater():
    permissions = {"permission": 5}
    if_lesser(permissions, "permission", 6)
    assert permissions == {"permission": 5}


def test_if_lesser_changes_permission_if_value_is_lesser():
    permissions = {"permission": 5}
    if_lesser(permissions, "permission", 4)
    assert permissions == {"permission": 4}


def test_if_zero_or_greater_keeps_permission_high_if_value_is_lesser():
    permissions = {"permission": 5}
    if_zero_or_greater(permissions, "permission", 4)
    assert permissions == {"permission": 5}


def test_if_zero_or_greater_changes_permission_if_value_is_greater():
    permissions = {"permission": 5}
    if_zero_or_greater(permissions, "permission", 6)
    assert permissions == {"permission": 6}


def test_if_zero_or_greater_changes_permission_if_value_is_zero():
    permissions = {"permission": 5}
    if_zero_or_greater(permissions, "permission", 0)
    assert permissions == {"permission": 0}
