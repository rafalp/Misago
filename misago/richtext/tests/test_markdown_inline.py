from unittest.mock import ANY

import pytest

from ..parser import parse_markup


@pytest.mark.asyncio
async def test_emphasis_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello *world*!")
    assert result == [{"id": ANY, "type": "p", "text": "Hello <em>world</em>!"}]


@pytest.mark.asyncio
async def test_emphasis_alt_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello _world_!")
    assert result == [{"id": ANY, "type": "p", "text": "Hello <em>world</em>!"}]


@pytest.mark.asyncio
async def test_strong_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello **world**!")
    assert result == [{"id": ANY, "type": "p", "text": "Hello <strong>world</strong>!"}]


@pytest.mark.asyncio
async def test_strong_alt_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello __world__!")
    assert result == [{"id": ANY, "type": "p", "text": "Hello <strong>world</strong>!"}]


@pytest.mark.asyncio
async def test_strikethrough_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello ~~world~~!")
    assert result == [{"id": ANY, "type": "p", "text": "Hello <del>world</del>!"}]


@pytest.mark.asyncio
async def test_inline_code_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello `world`!")
    assert result == [{"id": ANY, "type": "p", "text": "Hello <code>world</code>!"}]


@pytest.mark.asyncio
async def test_inline_code_is_escaped(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello `<b>world</b>`!")
    assert result == [
        {"id": ANY, "type": "p", "text": "Hello <code>&lt;b&gt;world&lt;/b&gt;</code>!"}
    ]


@pytest.mark.asyncio
async def test_simple_link_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "See <http://google.com>!")
    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": (
                'See <a href="http://google.com" rel="nofollow">'
                "http://google.com</a>!"
            ),
        }
    ]


@pytest.mark.asyncio
async def test_literal_link_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "See http://google.com")
    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": (
                'See <a href="http://google.com" rel="nofollow">http://google.com</a>'
            ),
        }
    ]


@pytest.mark.asyncio
async def test_link_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "See [here](http://google.com)!")
    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": 'See <a href="http://google.com" rel="nofollow">here</a>!',
        }
    ]


@pytest.mark.asyncio
async def test_image_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "See ![logo](http://google.com)!")
    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": 'See <img src="http://google.com" alt="logo" />!',
        }
    ]


@pytest.mark.asyncio
async def test_short_image_markdown_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "See !(http://google.com)!")
    assert result == [
        {"id": ANY, "type": "p", "text": 'See <img src="http://google.com" alt="" />!',}
    ]


@pytest.mark.asyncio
async def test_hard_linebreak_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello\nWorld!")
    assert result == [{"id": ANY, "type": "p", "text": "Hello<br/>World!",}]
