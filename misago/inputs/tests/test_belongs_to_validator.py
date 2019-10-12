import pytest

from ..errors import InputError
from ..validators import BelongsToValidator


def test_belongs_to_validator_raises_invalid_error_for_invalid_value():
    validator = BelongsToValidator([1, 2, 3])
    with pytest.raises(InputError) as excinfo:
        validator(4)

    assert excinfo.value.code == "INVALID"


def test_inverse_belongs_to_validator_raises_invalid_error_for_invalid_value():
    validator = BelongsToValidator([1, 2, 3], inverse_match=True)
    with pytest.raises(InputError) as excinfo:
        validator(2)

    assert excinfo.value.code == "INVALID"


def test_belongs_to_validator_raises_custom_code_for_invalid_value():
    validator = BelongsToValidator([1, 2, 3], code="CUSTOM")
    with pytest.raises(InputError) as excinfo:
        validator(4)

    assert excinfo.value.code == "CUSTOM"


def test_belongs_to_validator_allows_value_within_choices():
    validator = BelongsToValidator([1, 2, 3])
    validator(2)
