import pytest
from django.core.exceptions import ValidationError

from ..validators import validate_poll_choices


def test_validate_poll_choices_validates_valid_choices():
    validate_poll_choices(
        [
            {
                "id": "aaaaaaaaaaaa",
                "name": "lorem",
                "votes": 0,
            },
            {
                "id": "bbbbbbbbbbbb",
                "name": "ipsum",
                "votes": 0,
            },
        ],
        max_choices=2,
        choice_min_length=1,
        choice_max_length=20,
    )


def test_validate_poll_choices_raises_validation_error_if_choices_number_is_exceeded():
    with pytest.raises(ValidationError) as exc_info:
        validate_poll_choices(
            [
                {
                    "id": "aaaaaaaaaaaa",
                    "name": "lorem",
                    "votes": 0,
                },
                {
                    "id": "bbbbbbbbbbbb",
                    "name": "ipsum",
                    "votes": 0,
                },
                {
                    "id": "cccccccccccc",
                    "name": "dolor",
                    "votes": 0,
                },
            ],
            max_choices=2,
            choice_min_length=1,
            choice_max_length=20,
        )

    assert str(exc_info.value.message) == (
        "Poll cannot have more than %(limit_value)s choices "
        "(it currently has %(show_value)s)."
    )
    assert exc_info.value.code == "max_choices"
    assert exc_info.value.params == {"limit_value": 2, "show_value": 3}


def test_validate_poll_choices_raises_validation_error_if_choice_is_too_short():
    with pytest.raises(ValidationError) as exc_info:
        validate_poll_choices(
            [
                {
                    "id": "aaaaaaaaaaaa",
                    "name": "lorem",
                    "votes": 0,
                },
                {
                    "id": "bbbbbbbbbbbb",
                    "name": "ip",
                    "votes": 0,
                },
                {
                    "id": "cccccccccccc",
                    "name": "dolor",
                    "votes": 0,
                },
            ],
            max_choices=3,
            choice_min_length=3,
            choice_max_length=20,
        )

    assert exc_info.value.messages == [
        '"ip": choice should be at least 3 characters long (it has 2).'
    ]


def test_validate_poll_choices_raises_validation_error_if_choice_is_too_long():
    with pytest.raises(ValidationError) as exc_info:
        validate_poll_choices(
            [
                {
                    "id": "aaaaaaaaaaaa",
                    "name": "lorem",
                    "votes": 0,
                },
                {
                    "id": "bbbbbbbbbbbb",
                    "name": "ipsum",
                    "votes": 0,
                },
                {
                    "id": "cccccccccccc",
                    "name": "dolormet",
                    "votes": 0,
                },
            ],
            max_choices=3,
            choice_min_length=3,
            choice_max_length=5,
        )

    assert exc_info.value.messages == [
        '"dolormet": choice cannot exceed 5 characters (it has 8).'
    ]


def test_validate_poll_choices_skips_duplicate_errors():
    with pytest.raises(ValidationError) as exc_info:
        validate_poll_choices(
            [
                {
                    "id": "aaaaaaaaaaaa",
                    "name": "",
                    "votes": 0,
                },
                {
                    "id": "bbbbbbbbbbbb",
                    "name": "",
                    "votes": 0,
                },
                {
                    "id": "cccccccccccc",
                    "name": "dolor",
                    "votes": 0,
                },
            ],
            max_choices=3,
            choice_min_length=3,
            choice_max_length=10,
        )

    assert exc_info.value.messages == ["Edited poll choice can't be empty."]
