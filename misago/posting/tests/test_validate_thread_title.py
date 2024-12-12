import pytest
from django.core.exceptions import ValidationError

from ..validators import validate_thread_title


def test_validate_thread_title_passes_valid_value():
    validate_thread_title("valid value", 1, 100)


def test_validate_thread_title_raises_error_for_empty_value():
    with pytest.raises(ValidationError) as exc_info:
        validate_thread_title("", 1, 100)

    assert str(exc_info.value.message) == "Enter a thread title."
    assert exc_info.value.code == "required"


def test_validate_thread_title_raises_error_for_too_short_value():
    with pytest.raises(ValidationError) as exc_info:
        validate_thread_title("short", 10, 100)

    assert str(exc_info.value.message) == (
        "Thread title should be at least %(limit_value)s "
        "characters long (it has %(show_value)s)."
    )
    assert exc_info.value.code == "min_length"
    assert exc_info.value.params == {"limit_value": 10, "show_value": 5}


def test_validate_thread_title_raises_error_for_too_long_value():
    with pytest.raises(ValidationError) as exc_info:
        validate_thread_title("lorem ipsum dolor met", 1, 10)

    assert str(exc_info.value.message) == (
        "Thread title cannot exceed %(limit_value)s "
        "characters (it currently has %(show_value)s)."
    )
    assert exc_info.value.code == "max_length"
    assert exc_info.value.params == {"limit_value": 10, "show_value": 21}


def test_validate_thread_title_raises_error_for_value_missing_alphanumerics():
    with pytest.raises(ValidationError) as exc_info:
        validate_thread_title("!!!!!", 1, 10)

    assert str(exc_info.value.message) == (
        "Thread title must include alphanumeric characters."
    )
    assert exc_info.value.code == "invalid"
