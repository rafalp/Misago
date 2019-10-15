import pytest

from ..errors import InputError
from ..validators import MaxValueValidator


def test_value_validator_raises_too_large_error_for_invalid_value():
    validator = MaxValueValidator(3)
    with pytest.raises(InputError) as excinfo:
        validator(4)

    assert excinfo.value.code == "TOO_LARGE"


def test_value_validator_raises_custom_code_for_invalid_value():
    validator = MaxValueValidator(3, code="CUSTOM")
    with pytest.raises(InputError) as excinfo:
        validator(4)

    assert excinfo.value.code == "CUSTOM"


def test_value_validator_allows_value_equal_to_max_value():
    validator = MaxValueValidator(3)
    validator(3)


def test_value_validator_allows_value_less_than_max_value():
    validator = MaxValueValidator(3)
    validator(2)
