import pytest

from ..errors import InputError
from ..validators import MaxLengthValidator


def test_length_validator_raises_too_large_error_for_invalid_value():
    validator = MaxLengthValidator(3)
    with pytest.raises(InputError) as excinfo:
        validator("abcd")

    assert excinfo.value.code == "TOO_LARGE"


def test_length_validator_raises_custom_code_for_invalid_value():
    validator = MaxLengthValidator(3, code="CUSTOM")
    with pytest.raises(InputError) as excinfo:
        validator("abcd")

    assert excinfo.value.code == "CUSTOM"


def test_length_validator_allows_value_equal_to_max_length():
    validator = MaxLengthValidator(3)
    validator("abc")


def test_length_validator_allows_value_shorter_than_max_length():
    validator = MaxLengthValidator(3)
    validator("ab")
