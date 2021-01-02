from unittest.mock import ANY

import pytest

from ..parser import parse_markup


@pytest.mark.asyncio
async def test_bold_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello [b]world[/b]!")
    assert result == [{"id": ANY, "type": "p", "text": "Hello <b>world</b>!"}]


@pytest.mark.asyncio
async def test_italics_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello [i]world[/i]!")
    assert result == [{"id": ANY, "type": "p", "text": "Hello <i>world</i>!"}]


@pytest.mark.asyncio
async def test_underline_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello [u]world[/u]!")
    assert result == [{"id": ANY, "type": "p", "text": "Hello <u>world</u>!"}]


@pytest.mark.asyncio
async def test_strikethrough_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello [s]world[/s]!")
    assert result == [{"id": ANY, "type": "p", "text": "Hello <del>world</del>!"}]


@pytest.mark.asyncio
async def test_subscript_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello [sub]world[/sub]!")
    assert result == [{"id": ANY, "type": "p", "text": "Hello <sub>world</sub>!"}]


@pytest.mark.asyncio
async def test_superscript_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "Hello [sup]world[/sup]!")
    assert result == [{"id": ANY, "type": "p", "text": "Hello <sup>world</sup>!"}]


@pytest.mark.asyncio
async def test_link_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "See [url]http://google.com[/url]!")
    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": (
                'See <a href="http://google.com" rel="nofollow">http://google.com</a>!'
            ),
        }
    ]


@pytest.mark.asyncio
async def test_named_link_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(
        graphql_context, "See [url=http://google.com]Google[/url]!"
    )
    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": ('See <a href="http://google.com" rel="nofollow">Google</a>!'),
        }
    ]


@pytest.mark.asyncio
async def test_named_link_with_markup_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(
        graphql_context, "See [url=http://google.com]*Google*[/url]!"
    )
    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": (
                'See <a href="http://google.com" rel="nofollow"><em>Google</em></a>!'
            ),
        }
    ]


@pytest.mark.asyncio
async def test_named_link_bbcode_handles_link_children(graphql_context):
    result, _ = await parse_markup(
        graphql_context, "See [url=http://google.com]http://onet.pl[/url]!"
    )
    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": (
                'See <a href="http://google.com" rel="nofollow">http://onet.pl</a>!'
            ),
        }
    ]


@pytest.mark.asyncio
async def test_named_link_bbcode_handles_auto_link_children(graphql_context):
    result, _ = await parse_markup(
        graphql_context, "See [url=http://google.com]<http://onet.pl>[/url]!"
    )
    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": (
                'See <a href="http://google.com" rel="nofollow">&lt;http://onet.pl&gt;</a>!'
            ),
        }
    ]


@pytest.mark.asyncio
async def test_img_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(
        graphql_context, "See [img]http://google.com/logo.jpg[/img]!"
    )
    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": ('See <img src="http://google.com/logo.jpg" alt="" />!'),
        }
    ]


@pytest.mark.asyncio
async def test_titled_img_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(
        graphql_context, "See [img=http://google.com/logo.jpg]Title[/img]!"
    )
    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": ('See <img src="http://google.com/logo.jpg" alt="Title" />!'),
        }
    ]
