from typing import Callable

from django.contrib.auth import get_user_model
from django.http import HttpRequest

from .hooks import create_parser_hook
from .parser import Parser, Pattern
from .patterns import block_patterns, inline_patterns

User = get_user_model()


def create_parser(
    *,
    user: User | None = None,
    request: HttpRequest | None = None,
    content_type: str | None = None,
) -> Parser:
    return create_parser_hook(
        _create_parser_action,
        block_patterns=block_patterns.copy(),
        inline_patterns=inline_patterns.copy(),
        post_processors=[],
        user=user,
        request=request,
        content_type=content_type,
    )


def _create_parser_action(
    *,
    block_patterns: list[Pattern],
    inline_patterns: list[Pattern],
    post_processors: list[Callable[[Parser, list[dict]], list[dict]]],
    user: User | None = None,
    request: HttpRequest | None = None,
    content_type: str | None = None,
) -> Parser:
    return Parser(block_patterns, inline_patterns, post_processors)
