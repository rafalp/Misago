import pytest
from django.core.exceptions import ValidationError

from ..validators import validate_poll_question


def test_validate_poll_question_validates_question():
    validate_poll_question("Valid question", min_length=3, max_length=150)


def test_validate_poll_question_raises_validation_error_if_question_is_too_short():
    with pytest.raises(ValidationError) as exc_info:
        validate_poll_question("Valid", min_length=10, max_length=150)

    assert str(exc_info.value.message) == (
        "Poll question should be at least %(limit_value)s characters long "
        "(it has %(show_value)s)."
    )
    assert exc_info.value.code == "min_length"
    assert exc_info.value.params == {"limit_value": 10, "show_value": 5}


def test_validate_poll_question_raises_validation_error_if_question_is_too_long():
    with pytest.raises(ValidationError) as exc_info:
        validate_poll_question("Lorem ipsum dolor", min_length=5, max_length=10)

    assert str(exc_info.value.message) == (
        "Poll question cannot exceed %(limit_value)s characters "
        "(it currently has %(show_value)s)."
    )
    assert exc_info.value.code == "max_length"
    assert exc_info.value.params == {"limit_value": 10, "show_value": 17}
