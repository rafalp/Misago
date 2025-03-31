from markdown_it import MarkdownIt
from markdown_it.token import Token


def tokenize(parser: MarkdownIt, markup: str) -> list[Token]:
    return _tokenize_action(parser, markup)


def _tokenize_action(parser: MarkdownIt, markup: str) -> list[Token]:
    tokens = parser.parse(markup)
    return tokens
