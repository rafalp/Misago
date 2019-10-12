import re

import pytest

from ..errors import InputError
from ..validators import RegexValidator


def test_regex_validator_raises_invalid_error_for_invalid_value():
    validator = RegexValidator("[0-9]+")
    with pytest.raises(InputError) as excinfo:
        validator("abcd")

    assert excinfo.value.code == "INVALID"


def test_inverse_regex_validator_raises_invalid_error_for_invalid_value():
    validator = RegexValidator("[0-9]+", inverse_match=True)
    with pytest.raises(InputError) as excinfo:
        validator("1234")

    assert excinfo.value.code == "INVALID"


def test_regex_validator_raises_custom_code_for_invalid_value():
    validator = RegexValidator("[0-9]+", code="CUSTOM")
    with pytest.raises(InputError) as excinfo:
        validator("abcd")

    assert excinfo.value.code == "CUSTOM"


def test_regex_validator_raises_type_error_when_initialized_with_compiled_regex_and_flags():
    compiled = re.compile("[0-9]+")
    with pytest.raises(TypeError):
        RegexValidator(compiled, flags=re.IGNORECASE)


def test_regex_validator_uses_compiled_regex_to_validate_values():
    validator = RegexValidator(re.compile("a+"))
    with pytest.raises(InputError) as excinfo:
        validator("bbb")

    assert excinfo.value.code == "INVALID"


def test_regex_validator_uses_flags_validate_values():
    validator = RegexValidator("a+", flags=re.IGNORECASE)
    validator("AAA")


def test_regex_validator_passess_valid_value():
    validator = RegexValidator("[0-9]+")
    validator("2077")
