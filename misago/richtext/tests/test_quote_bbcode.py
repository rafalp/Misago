from unittest.mock import ANY

import pytest

from ..parser import parse_markup


@pytest.mark.asyncio
async def test_quote_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "[quote]Hello world![/quote]")
    assert result == [
        {
            "id": ANY,
            "type": "quote",
            "author": None,
            "post": None,
            "children": [{"id": ANY, "type": "p", "text": "Hello world!"}],
        }
    ]


@pytest.mark.asyncio
async def test_quote_with_author_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "[quote=Bob]Hello world![/quote]")
    assert result == [
        {
            "id": ANY,
            "type": "quote",
            "author": {"id": None, "name": "Bob", "slug": None},
            "post": None,
            "children": [{"id": ANY, "type": "p", "text": "Hello world!"}],
        }
    ]


@pytest.mark.asyncio
async def test_quote_with_author_and_post_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(
        graphql_context, "[quote=Bob:1421]Hello world![/quote]"
    )
    assert result == [
        {
            "id": ANY,
            "type": "quote",
            "author": {"id": None, "name": "Bob", "slug": None},
            "post": 1421,
            "children": [{"id": ANY, "type": "p", "text": "Hello world!"}],
        }
    ]
