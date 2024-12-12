from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import npgettext_lazy, pgettext_lazy

from ..core.utils import slugify
from .hooks import (
    validate_thread_title_hook,
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
            message=pgettext_lazy(
                "thread title validator", "You have to enter a thread title."
            ),
            code="thread_title_required",
        )

    slug = slugify(value)

    if not slug.replace("-", ""):
        raise ValidationError(
            message=pgettext_lazy(
                "thread title validator",
                "Thread title must include alphanumeric characters.",
            ),
            code="thread_title_missing_alphanumerics",
        )

    if length < min_length:
        raise ValidationError(
            message=npgettext_lazy(
                "thread title validator",
                "Thread title should be at least %(limit_value)s character long (it has %(show_value)s).",
                "Thread title should be at least %(limit_value)s characters long (it has %(show_value)s).",
                min_length,
            ),
            code="thread_title_too_short",
            params={
                "limit_value": min_length,
                "show_value": length,
            },
        )

    if length > max_length:
        raise ValidationError(
            message=npgettext_lazy(
                "thread title validator",
                "Thread title cannot exceed %(limit_value)s character (it currently has %(show_value)s).",
                "Thread title cannot exceed %(limit_value)s characters (it currently has %(show_value)s).",
                max_length,
            ),
            code="thread_title_too_short",
            params={
                "limit_value": min_length,
                "show_value": length,
            },
        )
