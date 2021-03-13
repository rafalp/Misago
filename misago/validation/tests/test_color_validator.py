import pytest
from pydantic.errors import ColorError

from ..validators import color_validator


def test_color_validator_returns_hex_color_for_valid_color_name():
    assert color_validator("green") == "#008000"


def test_color_validator_returns_hex_color_for_valid_color_hex():
    assert color_validator("#ff0000") == "#F00"


def test_color_validator_raises_error_for_invalid_color_value():
    with pytest.raises(ColorError):
        assert color_validator("nopez")
