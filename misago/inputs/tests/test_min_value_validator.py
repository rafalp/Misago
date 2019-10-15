import pytest

from ..errors import InputError
from ..validators import MinValueValidator


def test_value_validator_raises_too_small_error_for_invalid_value():
    validator = MinValueValidator(3)
    with pytest.raises(InputError) as excinfo:
        validator(2)

    assert excinfo.value.code == "TOO_SMALL"


def test_value_validator_raises_custom_code_for_invalid_value():
    validator = MinValueValidator(3, code="CUSTOM")
    with pytest.raises(InputError) as excinfo:
        validator(2)

    assert excinfo.value.code == "CUSTOM"


def test_value_validator_allows_value_equal_to_min_value():
    validator = MinValueValidator(3)
    validator(3)


def test_value_validator_allows_value_greater_than_min_value():
    validator = MinValueValidator(3)
    validator(4)
