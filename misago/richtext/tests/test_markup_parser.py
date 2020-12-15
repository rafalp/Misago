from unittest.mock import ANY
import pytest

from ..parser import parse_markup


@pytest.mark.asyncio
async def test_parser_parses_simple_paragraph(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello world!")
    assert result == [{"id": ANY, "type": "p", "text": "Hello world!"}]


@pytest.mark.asyncio
async def test_parser_parses_complex_paragraph(graphql_context):
    result, _ = await parse_markup(
        graphql_context,
        "Hello **world**, can [you _just_ google](http://google.com) it?",
    )

    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": (
                "Hello <strong>world</strong>, "
                'can <a href="http://google.com" rel="nofollow">'
                "you <em>just</em> google</a> it?"
            ),
        }
    ]


@pytest.mark.asyncio
async def test_parser_escapes_html(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello <b>world</b>!")
    assert result == [
        {"id": ANY, "type": "p", "text": "Hello &lt;b&gt;world&lt;/b&gt;!"}
    ]
