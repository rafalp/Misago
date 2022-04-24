import pytest

from ..cleanarg import clean_id_arg
from ..exceptions import InvalidArgumentError


def test_valid_id_arg_value_is_cleaned():
    assert clean_id_arg("13") == 13


def test_invalid_argument_error_is_raised_for_invalid_id():
    with pytest.raises(InvalidArgumentError):
        clean_id_arg("invalid")


def test_invalid_argument_error_is_raised_for_zero_id():
    with pytest.raises(InvalidArgumentError):
        clean_id_arg("0")


def test_invalid_argument_error_is_raised_for_negative_id():
    with pytest.raises(InvalidArgumentError):
        clean_id_arg("-1")


def test_invalid_argument_error_is_raised_for_empty_id():
    with pytest.raises(InvalidArgumentError):
        clean_id_arg(None)


def test_invalid_argument_error_is_raised_for_empty_str_id():
    with pytest.raises(InvalidArgumentError):
        clean_id_arg(" ")
