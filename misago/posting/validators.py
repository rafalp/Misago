from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import npgettext, pgettext

from ..core.utils import slugify
from .floodcontrol import flood_control
from .hooks import (
    validate_post_hook,
    validate_posted_contents_hook,
    validate_thread_title_hook,
)

if TYPE_CHECKING:
    from .formsets import PostingFormset
    from .state import PostingState


__all__ = [
    "validate_flood_control",
    "validate_post",
    "validate_posted_contents",
    "validate_thread_title",
]


def validate_post(
    value: str,
    min_length: int,
    max_length: int,
    *,
    request: HttpRequest | None = None,
):
    validate_post_hook(
        _validate_post_action,
        value,
        min_length,
        max_length,
        request=request,
    )


def _validate_post_action(
    value: str,
    min_length: int,
    max_length: int,
    *,
    request: HttpRequest | None = None,
):
    length = len(value)
    if not length:
        raise ValidationError(
            message=pgettext("post validator", "Enter post's content."),
            code="required",
        )

    if length < min_length:
        raise ValidationError(
            message=npgettext(
                "post validator",
                "Posted message must be at least %(limit_value)s character long (it has %(show_value)s).",
                "Posted message must be at least %(limit_value)s characters long (it has %(show_value)s).",
                min_length,
            ),
            code="min_length",
            params={
                "limit_value": min_length,
                "show_value": length,
            },
        )

    if max_length and length > max_length:
        raise ValidationError(
            message=npgettext(
                "post validator",
                "Posted message cannot be longer than %(limit_value)s character (it currently has %(show_value)s).",
                "Posted message cannot be longer than %(limit_value)s characters (it currently has %(show_value)s).",
                max_length,
            ),
            code="max_length",
            params={
                "limit_value": max_length,
                "show_value": length,
            },
        )


def validate_thread_title(
    value: str,
    min_length: int,
    max_length: int,
    *,
    request: HttpRequest | None = None,
):
    validate_thread_title_hook(
        _validate_thread_title_action,
        value,
        min_length,
        max_length,
        request=request,
    )


def _validate_thread_title_action(
    value: str,
    min_length: int,
    max_length: int,
    *,
    request: HttpRequest | None = None,
):
    length = len(value)
    if not length:
        raise ValidationError(
            message=pgettext("thread title validator", "Enter a thread title."),
            code="required",
        )

    slug = slugify(value)

    if not slug.replace("-", ""):
        raise ValidationError(
            message=pgettext(
                "thread title validator",
                "Thread title must include alphanumeric characters.",
            ),
            code="invalid",
        )

    if length < min_length:
        raise ValidationError(
            message=npgettext(
                "thread title validator",
                "Thread title should be at least %(limit_value)s character long (it has %(show_value)s).",
                "Thread title should be at least %(limit_value)s characters long (it has %(show_value)s).",
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
                "thread title validator",
                "Thread title cannot exceed %(limit_value)s character (it currently has %(show_value)s).",
                "Thread title cannot exceed %(limit_value)s characters (it currently has %(show_value)s).",
                max_length,
            ),
            code="max_length",
            params={
                "limit_value": max_length,
                "show_value": length,
            },
        )


def validate_posted_contents(formset: "PostingFormset", state: "PostingState") -> bool:
    validate_posted_contents_hook(formset, state)
    return not bool(formset.errors)


def validate_flood_control(formset: "PostingFormset", state: "PostingState") -> bool:
    try:
        flood_control(state.request)
    except ValidationError as e:
        formset.add_error(e)
    return not bool(formset.errors)
