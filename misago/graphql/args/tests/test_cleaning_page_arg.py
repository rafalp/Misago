import pytest

from ..cleanarg import clean_page_arg
from ..exceptions import InvalidArgumentError


def test_empty_page_arg_value_is_cleaned():
    assert clean_page_arg(None) == 1


def test_valid_page_arg_value_is_cleaned():
    assert clean_page_arg(123) == 123


def test_valid_page_arg_value_str_is_cleaned():
    assert clean_page_arg("123") == 123


def test_invalid_argument_error_is_raised_for_zero_page():
    with pytest.raises(InvalidArgumentError):
        clean_page_arg(0)


def test_invalid_argument_error_is_raised_for_negative_page():
    with pytest.raises(InvalidArgumentError):
        clean_page_arg(-1)


def test_invalid_argument_error_is_raised_for_invalid_page():
    with pytest.raises(InvalidArgumentError):
        clean_page_arg("invalid")


def test_invalid_argument_error_is_raised_for_empty_str_page():
    with pytest.raises(InvalidArgumentError):
        clean_page_arg(" ")
