from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext

from ..threads.models import Post
from .hooks import validate_thread_solution_hook


def is_valid_thread_solution(post: Post, request: HttpRequest | None = None) -> bool:
    try:
        validate_thread_solution(post, request)
        return True
    except ValidationError:
        return False


def validate_thread_solution(post: Post, request: HttpRequest | None = None):
    validate_thread_solution_hook(_validate_thread_solution_action, post, request)


def _validate_thread_solution_action(post: Post, request: HttpRequest | None = None):
    if post.is_hidden:
        raise ValidationError(
            message=pgettext(
                "thread solution validator",
                "Hidden posts can't be selected as thread solutions.",
            ),
            code="post_hidden",
        )

    if post.is_unapproved:
        raise ValidationError(
            message=pgettext(
                "thread solution validator",
                "Unapproved posts can't be selected as thread solutions.",
            ),
            code="post_unapproved",
        )
