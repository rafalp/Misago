from typing import Iterable

from django.core.exceptions import ValidationError
from django.utils.translation import npgettext, pgettext

from .choices import PollChoices


def validate_poll_vote(
    user_choices: Iterable[str],
    poll_choices: PollChoices,
    max_choices: int,
) -> set[str]:
    if not user_choices:
        raise ValidationError(
            message=pgettext("poll vote validator", "Select a choice"),
            code="required",
        )

    valid_choices = set(poll_choices.ids()).intersection(user_choices)

    if not valid_choices:
        raise ValidationError(
            message=pgettext("poll vote validator", "Invalid choice"),
            code="invalid",
        )

    if len(valid_choices) > max_choices:
        raise ValidationError(
            npgettext(
                "poll vote validator",
                "Select no more than %(choices)s choice",
                "Select no more than %(choices)s choices",
                max_choices,
            ),
            code="max_choices",
            params={"choices": max_choices},
        )

    return valid_choices
