import pytest
from django.core.exceptions import ValidationError

from ..choices import PollChoices
from ..validators import validate_poll_vote

poll_choices: PollChoices = [
    {"id": "aa", "name": "first", "votes": 0},
    {"id": "bb", "name": "second", "votes": 0},
    {"id": "cc", "name": "third", "votes": 0},
    {"id": "dd", "name": "fourth", "votes": 0},
]


def test_validate_poll_vote_passes_valid_choices():
    valid_choices = validate_poll_vote(["aa", "bb"], poll_choices, 2)
    assert valid_choices == {"aa", "bb"}


def test_validate_poll_vote_passes_partially_valid_choices():
    valid_choices = validate_poll_vote(["bb", "ee"], poll_choices, 2)
    assert valid_choices == {"bb"}


def test_validate_poll_vote_fails_for_empty_choices():
    with pytest.raises(ValidationError) as exc_info:
        validate_poll_vote([], poll_choices, 2)

    assert exc_info.value.messages == ["Select a choice."]
    assert exc_info.value.code == "required"


def test_validate_poll_vote_fails_for_invalid_choices():
    with pytest.raises(ValidationError) as exc_info:
        validate_poll_vote(["ee"], poll_choices, 2)

    assert exc_info.value.messages == ["Invalid choice."]
    assert exc_info.value.code == "invalid"


def test_validate_poll_vote_fails_for_too_many_choices():
    with pytest.raises(ValidationError) as exc_info:
        validate_poll_vote(["aa", "bb", "cc"], poll_choices, 2)

    assert exc_info.value.messages == ["Select no more than 2 choices."]
    assert exc_info.value.code == "max_choices"
