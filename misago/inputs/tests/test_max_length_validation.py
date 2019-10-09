import pytest

from ..errors import InputError
from ..validators import validate_max_length


def test_length_validator_raises_too_long_error_for_invalid_value():
    validator = validate_max_length(3)
    with pytest.raises(InputError) as excinfo:
        validator("abcd")

    assert excinfo.value.code == "TOO_LONG"


def test_length_validator_includes_detail_in_raised_error():
    validator = validate_max_length(3)
    with pytest.raises(InputError) as excinfo:
        validator("abcd")

    assert excinfo.value.detail == "4 > 3"


def test_length_validator_allows_value_equal_to_max_length():
    validator = validate_max_length(3)
    validator("abc")


def test_length_validator_allows_value_shorter_than_max_length():
    validator = validate_max_length(3)
    validator("ab")
