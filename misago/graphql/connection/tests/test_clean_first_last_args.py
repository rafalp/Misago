import pytest

from ..cleanargs import ValidationError, clean_first_last


def test_validation_error_is_raised_if_first_and_last_are_not_set():
    with pytest.raises(ValidationError):
        clean_first_last({}, 100)


def test_validation_error_is_raised_if_first_and_last_are_both_set():
    with pytest.raises(ValidationError):
        clean_first_last({"first": 0, "last": 0}, 100)


def test_validation_error_is_raised_if_first_arg_is_negative():
    with pytest.raises(ValidationError):
        clean_first_last({"first": -1}, 100)


def test_validation_error_is_raised_if_first_arg_is_zero():
    with pytest.raises(ValidationError):
        clean_first_last({"first": 0}, 100)


def test_validation_error_is_raised_if_first_arg_is_greater_than_limit():
    with pytest.raises(ValidationError):
        clean_first_last({"first": 110}, 100)


def test_first_arg_is_cleaned_and_returned():
    first, last = clean_first_last({"first": 10}, 100)
    assert (first, last) == (10, None)


def test_validation_error_is_raised_if_last_arg_is_negative():
    with pytest.raises(ValidationError):
        clean_first_last({"last": -1}, 100)


def test_validation_error_is_raised_if_last_arg_is_zero():
    with pytest.raises(ValidationError):
        clean_first_last({"last": 0}, 100)


def test_validation_error_is_raised_if_last_arg_is_greater_than_limit():
    with pytest.raises(ValidationError):
        clean_first_last({"last": 110}, 100)


def test_last_arg_is_cleaned_and_returned():
    first, last = clean_first_last({"last": 10}, 100)
    assert (first, last) == (None, 10)
