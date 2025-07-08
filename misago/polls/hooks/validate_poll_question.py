from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook


class ValidatePollQuestionHookAction(Protocol):
    """
    Misago function for validating poll questions.
    Raises `ValidationError` if the poll question is invalid.

    # Arguments

    ## `value: str`

    The value to validate.

    ## `min_length: int`

    The minimum required length of the poll question.

    ## `max_length: int`

    The maximum allowed length of the poll question.

    ## `request: HttpRequest | None`

    The request object or `None` if not provided.
    """

    def __call__(
        self,
        value: str,
        min_length: int,
        max_length: int,
        request: HttpRequest | None = None,
    ) -> None: ...


class ValidatePollQuestionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: ValidatePollQuestionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `value: str`

    The value to validate.

    ## `min_length: int`

    The minimum required length of the poll question.

    ## `max_length: int`

    The maximum allowed length of the poll question.

    ## `request: HttpRequest | None`

    The request object or `None` if not provided.
    """

    def __call__(
        self,
        action: ValidatePollQuestionHookAction,
        value: str,
        min_length: int,
        max_length: int,
        request: HttpRequest | None = None,
    ) -> None: ...


class ValidatePollQuestionHook(
    FilterHook[
        ValidatePollQuestionHookAction,
        ValidatePollQuestionHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the standard logic used to
    validate poll questions.

    # Example

    Forbid selected words in poll questions:

    ```python
    from django.core.exceptions import ValidationError
    from django.http import HttpRequest
    from django.utils.translation import pgettext
    from misago.posting.hooks import validate_poll_question_hook

    BAD_WORDS = ("casino", "win", "spam")

    @validate_poll_question_hook.append_filter
    def validate_poll_question_bad_words(
        action,
        value: str,
        min_length: int,
        max_length: int,
        request: HttpRequest | None = None,
    ) -> None:
        value_lowercase = value.lower()
        for bad_word in BAD_WORDS:
            if bad_word in name_lowercase:
                raise ValidationError(
                    message=pgettext(
                        "poll question validator",
                        "This poll question is not allowed.",
                    ),
                    code="invalid",
                    params={"choice": choice},
                )

        action(
            choices,
            max_choices,
            choice_min_length,
            choice_max_length,
            request,
        )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: ValidatePollQuestionHookAction,
        value: str,
        min_length: int,
        max_length: int,
        request: HttpRequest | None = None,
    ) -> None:
        return super().__call__(
            action,
            value,
            min_length,
            max_length,
            request,
        )


validate_poll_question_hook = ValidatePollQuestionHook()
