import pytest

from ..errors import InputError
from ..validators import MinLengthValidator


def test_length_validator_raises_too_short_error_for_invalid_value():
    validator = MinLengthValidator(5)
    with pytest.raises(InputError) as excinfo:
        validator("abcd")

    assert excinfo.value.code == "TOO_SHORT"


def test_length_validator_raises_custom_code_for_invalid_value():
    validator = MinLengthValidator(5, code="CUSTOM")
    with pytest.raises(InputError) as excinfo:
        validator("abcd")

    assert excinfo.value.code == "CUSTOM"


def test_length_validator_includes_detail_in_raised_error():
    validator = MinLengthValidator(5)
    with pytest.raises(InputError) as excinfo:
        validator("abcd")

    assert excinfo.value.detail == "4 < 5"


def test_length_validator_allows_value_equal_to_min_length():
    validator = MinLengthValidator(5)
    validator("abcde")


def test_length_validator_allows_value_longer_than_min_length():
    validator = MinLengthValidator(5)
    validator("abcdefgh")
