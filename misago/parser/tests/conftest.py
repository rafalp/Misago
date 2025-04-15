import textwrap

import pytest

from ..factory import create_parser
from ..html import render_tokens_to_html
from ..tokenizer import tokenize


@pytest.fixture
def parse_to_html():
    def _parser(markup: str, dedent=False, strip=False):
        parser = create_parser()

        if dedent:
            markup = textwrap.dedent(markup)
        if strip:
            markup = markup.strip()

        tokens = tokenize(parser, markup)
        return render_tokens_to_html(parser, tokens)

    return _parser


@pytest.fixture
def parse_to_raw_tokens():
    def _parser(markup: str, dedent=False, strip=False):
        parser = create_parser()

        if dedent:
            markup = textwrap.dedent(markup)
        if strip:
            markup = markup.strip()

        return parser.parse(markup)

    return _parser
