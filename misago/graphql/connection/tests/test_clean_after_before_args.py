import pytest

from ....tables import users
from ..cleanargs import ValidationError, clean_after_before


def test_validation_error_is_raised_if_after_and_before_are_both_set():
    with pytest.raises(ValidationError):
        clean_after_before({"after": "a", "before": "b"}, users.c["slug"])


def test_validation_error_is_raised_if_after_value_is_not_valid_db_value():
    with pytest.raises(ValidationError):
        clean_after_before({"after": "a"}, users.c["id"])


def test_validation_error_is_raised_if_before_value_is_not_valid_db_value():
    with pytest.raises(ValidationError):
        clean_after_before({"before": "b"}, users.c["id"])


def test_validation_error_is_raised_if_after_value_is_negative_int():
    with pytest.raises(ValidationError):
        clean_after_before({"after": "-1"}, users.c["id"])


def test_validation_error_is_raised_if_before_value_is_negative_int():
    with pytest.raises(ValidationError):
        clean_after_before({"before": "-1"}, users.c["id"])


def test_validation_error_is_raised_if_after_value_is_zero_int():
    with pytest.raises(ValidationError):
        clean_after_before({"after": 0}, users.c["id"])


def test_validation_error_is_raised_if_before_value_is_zero_int():
    with pytest.raises(ValidationError):
        clean_after_before({"before": 0}, users.c["id"])


def test_valid_db_after_int_value_is_returned():
    after, before = clean_after_before({"after": "10"}, users.c["id"])
    assert (after, before) == (10, None)


def test_valid_db_before_int_value_is_returned():
    after, before = clean_after_before({"before": "10"}, users.c["id"])
    assert (after, before) == (None, 10)


def test_valid_db_after_str_value_is_returned():
    after, before = clean_after_before({"after": 10}, users.c["slug"])
    assert (after, before) == ("10", None)


def test_valid_db_before_str_value_is_returned():
    after, before = clean_after_before({"before": 10}, users.c["slug"])
    assert (after, before) == (None, "10")
