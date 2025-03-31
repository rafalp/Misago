from typing import Callable

from markdown_it import MarkdownIt
from markdown_it.token import Token

from .hooks import tokenize_hook


TokensProcessor = Callable[[list[Token]], list[Token] | None]


def tokenize(parser: MarkdownIt, markup: str) -> list[Token]:
    return tokenize_hook(_tokenize_action, parser, markup, [])


def _tokenize_action(
    parser: MarkdownIt,
    markup: str,
    processors: list[TokensProcessor],
) -> list[Token]:
    tokens = parser.parse(markup)
    for processor in processors:
        tokens = processor(tokens) or tokens
    return tokens


def tokenize_uwu(tokens: list[Token]) -> list[Token] | None:
    raise Exception(tokens)
    return tokens
