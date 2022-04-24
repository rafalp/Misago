import pytest

from ..cleanarg import clean_cursors_args
from ..exceptions import InvalidArgumentError


def test_no_after_and_before_args_are_handled():
    assert clean_cursors_args(None, None) == (None, None)


def test_invalid_argument_error_is_raised_is_both_after_and_before_args_are_set():
    with pytest.raises(InvalidArgumentError):
        clean_cursors_args(1, 2)


def test_valid_after_arg_value_is_cleaned():
    assert clean_cursors_args(1, None) == (1, None)


def test_valid_before_arg_value_is_cleaned():
    assert clean_cursors_args(None, 2) == (None, 2)


def test_invalid_argument_error_is_raised_for_invalid_after():
    with pytest.raises(InvalidArgumentError):
        clean_cursors_args("invalid", None)


def test_invalid_argument_error_is_raised_for_invalid_before():
    with pytest.raises(InvalidArgumentError):
        clean_cursors_args(None, "invalid")


def test_invalid_argument_error_is_raised_for_zero_after():
    with pytest.raises(InvalidArgumentError):
        clean_cursors_args("0", None)


def test_invalid_argument_error_is_raised_for_zero_before():
    with pytest.raises(InvalidArgumentError):
        clean_cursors_args(None, "0")


def test_invalid_argument_error_is_raised_for_negative_after():
    with pytest.raises(InvalidArgumentError):
        clean_cursors_args("-1", None)


def test_invalid_argument_error_is_raised_for_negative_before():
    with pytest.raises(InvalidArgumentError):
        clean_cursors_args(None, "-1")


def test_invalid_argument_error_is_raised_for_empty_str_after():
    with pytest.raises(InvalidArgumentError):
        clean_cursors_args(" ", None)


def test_invalid_argument_error_is_raised_for_empty_str_before():
    with pytest.raises(InvalidArgumentError):
        clean_cursors_args(None, " ")
