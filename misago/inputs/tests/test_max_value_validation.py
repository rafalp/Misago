import pytest

from ..errors import InputError
from ..validators import validate_max_value


def test_value_validator_raises_too_large_error_for_invalid_value():
    validator = validate_max_value(3)
    with pytest.raises(InputError) as excinfo:
        validator(4)

    assert excinfo.value.code == "TOO_LARGE"


def test_value_validator_includes_detail_in_raised_error():
    validator = validate_max_value(3)
    with pytest.raises(InputError) as excinfo:
        validator(4)

    assert excinfo.value.detail == "4 > 3"


def test_value_validator_allows_value_equal_to_max_value():
    validator = validate_max_value(3)
    validator(3)


def test_value_validator_allows_value_less_than_max_value():
    validator = validate_max_value(3)
    validator(2)
