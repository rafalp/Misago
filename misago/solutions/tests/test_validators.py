import pytest
from django.core.exceptions import ValidationError

from ..validators import is_valid_thread_solution, validate_thread_solution


def test_is_valid_thread_solution_returns_true_for_visible_post(reply):
    assert is_valid_thread_solution(reply)


def test_is_valid_thread_solution_returns_false_for_original_post(post):
    assert is_valid_thread_solution(post) is False


def test_is_valid_thread_solution_returns_false_for_hidden_post(reply):
    reply.is_hidden = True

    assert is_valid_thread_solution(reply) is False


def test_is_valid_thread_solution_returns_false_for_unapproved_post(reply):
    reply.is_unapproved = True

    assert is_valid_thread_solution(reply) is False


def test_is_valid_thread_solution_passes_visible_post(reply):
    validate_thread_solution(reply)


def test_is_valid_thread_solution_raises_validation_error_for_original_post(post):
    with pytest.raises(ValidationError):
        validate_thread_solution(post)


def test_is_valid_thread_solution_raises_validation_error_for_hidden_post(reply):
    reply.is_hidden = True

    with pytest.raises(ValidationError):
        validate_thread_solution(reply)


def test_is_valid_thread_solution_raises_validation_error_for_unapproved_post(reply):
    reply.is_unapproved = True

    with pytest.raises(ValidationError):
        validate_thread_solution(reply)
