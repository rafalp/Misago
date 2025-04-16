import pytest
from django.core.exceptions import ValidationError

from ...parser.parse import parse
from ..validators import validate_post


def test_validate_post_passes_valid_value():
    validate_post(parse("valid value"), 1, 100)


def test_validate_post_raises_error_for_empty_value():
    with pytest.raises(ValidationError) as exc_info:
        validate_post(parse(""), 1, 100)

    assert str(exc_info.value.message) == "Posted message has no content."
    assert exc_info.value.code == "required"


def test_validate_post_raises_error_for_too_short_value():
    with pytest.raises(ValidationError) as exc_info:
        validate_post(parse("short"), 10, 100)

    assert str(exc_info.value.message) == (
        "Posted message must be at least %(limit_value)s "
        "characters long (it has %(show_value)s)."
    )
    assert exc_info.value.code == "min_length"
    assert exc_info.value.params == {"limit_value": 10, "show_value": 5}


def test_validate_post_raises_error_for_too_long_value():
    with pytest.raises(ValidationError) as exc_info:
        validate_post(parse("lorem ipsum dolor met"), 1, 10)

    assert str(exc_info.value.message) == (
        "Posted message cannot be longer than %(limit_value)s "
        "characters (it currently has %(show_value)s)."
    )
    assert exc_info.value.code == "max_length"
    assert exc_info.value.params == {"limit_value": 10, "show_value": 21}


def test_validate_post_disables_max_length_validation():
    validate_post(parse("lorem ipsum dolor met"), 1, 0)
