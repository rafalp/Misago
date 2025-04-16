from dataclasses import dataclass

from markdown_it.token import Token

from .factory import create_parser
from .html import render_tokens_to_html
from .metadata import get_tokens_metadata
from .plaintext import render_tokens_to_plaintext
from .tokenizer import tokenize


@dataclass(frozen=True)
class ParsingResult:
    markup: str
    tokens: list[Token]
    html: str
    text: str
    metadata: dict


def parse(markup: str) -> ParsingResult:
    parser = create_parser()
    tokens = tokenize(parser, markup)

    return ParsingResult(
        markup=markup,
        tokens=tokens,
        html=render_tokens_to_html(parser, tokens),
        text=render_tokens_to_plaintext(tokens),
        metadata=get_tokens_metadata(tokens),
    )
