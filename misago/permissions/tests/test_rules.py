from ..enums import PermissionValue
from ..rules import yes_no_never, zero_or_greater


def test_yes_no_never_returns_false_if_value_is_false():
    assert yes_no_never([PermissionValue.NO, PermissionValue.NO]) is False


def test_yes_no_never_returns_true_if_any_value_is_true():
    assert yes_no_never([PermissionValue.NO, PermissionValue.YES]) is True


def test_yes_no_never_returns_false_if_any_value_is_never():
    assert yes_no_never([PermissionValue.NEVER, PermissionValue.YES]) is False


def test_zero_or_greater_returns_max_value_if_there_is_no_zero():
    assert zero_or_greater([2, 4, 1]) == 4


def test_zero_or_greater_returns_zero_if_its_present():
    assert zero_or_greater([2, 4, 0, 1]) == 0
