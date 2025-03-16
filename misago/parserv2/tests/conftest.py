import textwrap

import pytest

from ..factory import create_parser


@pytest.fixture
def parse_to_html():
    def _parser(markup: str, dedent=False, strip=False):
        parser = create_parser()

        if dedent:
            markup = textwrap.dedent(markup)
        if strip:
            markup = markup.strip()

        return parser.render(markup).strip()

    return _parser
