import pytest

from ..errors import InputError
from ..validators import validate_min_value


def test_value_validator_raises_too_small_error_for_invalid_value():
    validator = validate_min_value(3)
    with pytest.raises(InputError) as excinfo:
        validator(2)

    assert excinfo.value.code == "TOO_SMALL"


def test_value_validator_includes_detail_in_raised_error():
    validator = validate_min_value(3)
    with pytest.raises(InputError) as excinfo:
        validator(2)

    assert excinfo.value.detail == "2 < 3"


def test_value_validator_allows_value_equal_to_min_value():
    validator = validate_min_value(3)
    validator(3)


def test_value_validator_allows_value_greater_than_min_value():
    validator = validate_min_value(3)
    validator(4)
