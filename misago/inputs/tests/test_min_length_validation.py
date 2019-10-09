import pytest

from ..errors import InputError
from ..validators import validate_min_length


def test_length_validator_raises_too_short_error_for_invalid_value():
    validator = validate_min_length(5)
    with pytest.raises(InputError) as excinfo:
        validator("abcd")

    assert excinfo.value.code == "TOO_SHORT"


def test_length_validator_includes_detail_in_raised_error():
    validator = validate_min_length(5)
    with pytest.raises(InputError) as excinfo:
        validator("abcd")

    assert excinfo.value.detail == "4 < 5"


def test_length_validator_allows_value_equal_to_min_length():
    validator = validate_min_length(5)
    validator("abcde")


def test_length_validator_allows_value_longer_than_min_length():
    validator = validate_min_length(5)
    validator("abcdefgh")
