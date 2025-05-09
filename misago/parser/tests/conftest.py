import textwrap

import pytest

from ..factory import create_parser
from ..html import render_tokens_to_html
from ..tokenizer import tokenize


class MockGetRandomString:
    def __init__(self):
        self.calls = 0

    def __call__(self, *args):
        self.calls += 1
        return f"random{self.calls}"


@pytest.fixture
def mock_get_random_string(mocker):
    get_random_string = MockGetRandomString()
    mocker.patch("misago.parser.tokenizer.get_random_string", get_random_string)
    return get_random_string


@pytest.fixture
def parse_to_html(mock_get_random_string):
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
def parse_to_raw_tokens(mock_get_random_string):
    def _parser(markup: str, dedent=False, strip=False):
        parser = create_parser()

        if dedent:
            markup = textwrap.dedent(markup)
        if strip:
            markup = markup.strip()

        return parser.parse(markup)

    return _parser


@pytest.fixture
def parse_to_tokens(mock_get_random_string):
    def _parser(markup: str, dedent=False, strip=False):
        parser = create_parser()

        if dedent:
            markup = textwrap.dedent(markup)
        if strip:
            markup = markup.strip()

        return tokenize(parser, markup)

    return _parser
