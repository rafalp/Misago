from typing import Callable

from django.contrib.auth import get_user_model
from django.http import HttpRequest

from .hooks import create_parser
from .parser import MarkupParser, Pattern

User = get_user_model()


def create_parser(
    *,
    user: User | None = None,
    request: HttpRequest | None = None,
    content_type: str | None = None,
) -> MarkupParser:
    return create_parser(
        _create_parser_action,
        block_patterns=[],
        inline_patterns=[],
        user=user,
        request=request,
        content_type=content_type,
    )


def _create_parser_action(
    *,
    block_patterns: list[Pattern],
    inline_patterns: list[Pattern],
    user: User | None = None,
    request: HttpRequest | None = None,
    content_type: str | None = None,
) -> MarkupParser:
    return MarkupParser(block_patterns, inline_patterns)
