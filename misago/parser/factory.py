from typing import Callable

from django.contrib.auth import get_user_model

from .context import ParserContext
from .hooks import create_parser_hook
from .parser import Parser, Pattern
from .patterns import block_patterns, inline_patterns
from .postprocessors import post_processors

User = get_user_model()


def create_parser(context: ParserContext) -> Parser:
    return create_parser_hook(
        _create_parser_action,
        context,
        block_patterns=block_patterns.copy(),
        inline_patterns=inline_patterns.copy(),
        post_processors=post_processors.copy(),
    )


def _create_parser_action(
    context: ParserContext,
    *,
    block_patterns: list[Pattern],
    inline_patterns: list[Pattern],
    post_processors: list[Callable[[Parser, list[dict]], list[dict]]],
) -> Parser:
    return Parser(block_patterns, inline_patterns, post_processors)
