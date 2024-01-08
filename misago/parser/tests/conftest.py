from textwrap import dedent

import pytest

from ..factory import create_parser


@pytest.fixture
def parser():
    return create_parser()


@pytest.fixture
def parse_markup(parser):
    def parse_markup_func(markup: str) -> list[dict]:
        return parser(dedent(markup).strip())

    return parse_markup_func
