from typing import Iterable

from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import npgettext, pgettext

from .choices import PollChoices
from .hooks import (
    validate_poll_choices_hook,
    validate_poll_question_hook,
)


def validate_poll_question(
    value: str,
    min_length: int,
    max_length: int,
    request: HttpRequest | None = None,
):
    validate_poll_question_hook(
        _validate_poll_question_action,
        value,
        min_length,
        max_length,
        request,
    )


def _validate_poll_question_action(
    value: str,
    min_length: int,
    max_length: int,
    request: HttpRequest | None = None,
):
    length = len(value)

    if length < min_length:
        raise ValidationError(
            message=npgettext(
                "poll question validator",
                "Poll question should be at least %(limit_value)s character long (it has %(show_value)s).",
                "Poll question should be at least %(limit_value)s characters long (it has %(show_value)s).",
                min_length,
            ),
            code="min_length",
            params={
                "limit_value": min_length,
                "show_value": length,
            },
        )

    if length > max_length:
        raise ValidationError(
            message=npgettext(
                "poll question validator",
                "Poll question cannot exceed %(limit_value)s character (it currently has %(show_value)s).",
                "Poll question cannot exceed %(limit_value)s characters (it currently has %(show_value)s).",
                max_length,
            ),
            code="max_length",
            params={
                "limit_value": max_length,
                "show_value": length,
            },
        )


def validate_poll_choices(
    choices: PollChoices,
    max_choices: int,
    choice_min_length: int,
    choice_max_length: int,
    request: HttpRequest | None = None,
):
    validate_poll_choices_hook(
        _validate_poll_choices_action,
        choices,
        max_choices,
        choice_min_length,
        choice_max_length,
        request,
    )


def _validate_poll_choices_action(
    choices: PollChoices,
    max_choices: int,
    choice_min_length: int,
    choice_max_length: int,
    request: HttpRequest,
):
    choices_num = len(choices)
    if choices_num < 2:
        raise ValidationError(
            message=pgettext(
                "poll choices validator",
                "Poll must have at least two choices.",
            ),
            code="invalid",
        )

    if choices_num > max_choices:
        raise ValidationError(
            message=npgettext(
                "poll choices validator",
                "Poll cannot have more than %(limit_value)s choice (it currently has %(show_value)s).",
                "Poll cannot have more than %(limit_value)s choices (it currently has %(show_value)s).",
                max_choices,
            ),
            code="max_choices",
            params={
                "limit_value": max_choices,
                "show_value": choices_num,
            },
        )

    errors = []

    for name in [choice["name"] for choice in choices]:
        name_length = len(name)

        error = None
        if not name_length:
            error = ValidationError(
                message=pgettext(
                    "poll choices validator", "Edited poll choice can't be empty."
                ),
                code="min_length",
            )

        elif name_length < choice_min_length:
            error = ValidationError(
                message=npgettext(
                    "poll choices validator",
                    '"%(choice)s": choice should be at least %(limit_value)s character long (it has %(show_value)s).',
                    '"%(choice)s": choice should be at least %(limit_value)s characters long (it has %(show_value)s).',
                    choice_min_length,
                ),
                code="min_length",
                params={
                    "choice": name,
                    "limit_value": choice_min_length,
                    "show_value": name_length,
                },
            )

        elif name_length > choice_max_length:
            error = ValidationError(
                message=npgettext(
                    "poll choices validator",
                    '"%(choice)s": choice cannot exceed %(limit_value)s character (it has %(show_value)s).',
                    '"%(choice)s": choice cannot exceed %(limit_value)s characters (it has %(show_value)s).',
                    choice_max_length,
                ),
                code="max_length",
                params={
                    "choice": name,
                    "limit_value": choice_max_length,
                    "show_value": name_length,
                },
            )

        if error and error not in errors:
            errors.append(error)

    if errors:
        raise ValidationError(errors)


def validate_poll_vote(
    user_choices: Iterable[str],
    poll_choices: PollChoices,
    max_choices: int,
) -> set[str]:
    if not user_choices:
        raise ValidationError(
            message=pgettext("poll vote validator", "Select a choice."),
            code="required",
        )

    valid_choices = set(choice["id"] for choice in poll_choices).intersection(
        user_choices
    )

    if not valid_choices:
        raise ValidationError(
            message=pgettext("poll vote validator", "Invalid choice."),
            code="invalid",
        )

    if len(valid_choices) > max_choices:
        raise ValidationError(
            npgettext(
                "poll vote validator",
                "Select no more than %(choices)s choice.",
                "Select no more than %(choices)s choices.",
                max_choices,
            ),
            code="max_choices",
            params={"choices": max_choices},
        )

    return valid_choices
