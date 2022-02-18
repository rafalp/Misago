from unittest.mock import ANY

import pytest

from ..parser import parse_markup


@pytest.mark.asyncio
async def test_single_quote_block_is_restructured(context):
    result, _ = await parse_markup(context, "[quote]Hello world![/quote]")
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
async def test_sibling_quote_blocks_are_restructured(context):
    result, _ = await parse_markup(
        context, "[quote]Hello world![/quote]\n[quote]How is going?[/quote]"
    )
    assert result == [
        {
            "id": ANY,
            "type": "quote",
            "author": None,
            "post": None,
            "children": [{"id": ANY, "type": "p", "text": "Hello world!"}],
        },
        {
            "id": ANY,
            "type": "quote",
            "author": None,
            "post": None,
            "children": [{"id": ANY, "type": "p", "text": "How is going?"}],
        },
    ]


@pytest.mark.asyncio
async def test_nested_quote_blocks_are_restructured(context):
    result, _ = await parse_markup(
        context, "[quote]Hello world![quote]How is going?[/quote][/quote]"
    )
    assert result == [
        {
            "id": ANY,
            "type": "quote",
            "author": None,
            "post": None,
            "children": [
                {"id": ANY, "type": "p", "text": "Hello world!"},
                {
                    "id": ANY,
                    "type": "quote",
                    "author": None,
                    "post": None,
                    "children": [{"id": ANY, "type": "p", "text": "How is going?"}],
                },
            ],
        }
    ]


@pytest.mark.asyncio
async def test_invalid_opening_blocks_are_kept(context):
    result, _ = await parse_markup(context, "[quote]Hello world!")
    assert result == [
        {"id": ANY, "type": "p", "text": "[quote]"},
        {"id": ANY, "type": "p", "text": "Hello world!"},
    ]


@pytest.mark.asyncio
async def test_invalid_closing_blocks_are_kept(context):
    result, _ = await parse_markup(context, "Hello world![/quote]")
    assert result == [
        {"id": ANY, "type": "p", "text": "Hello world!"},
        {"id": ANY, "type": "p", "text": "[/quote]"},
    ]


@pytest.mark.asyncio
async def test_extra_opening_blocks_are_kept(context):
    result, _ = await parse_markup(context, "[quote]Hello [quote]world![/quote]")
    assert result == [
        {"id": ANY, "type": "p", "text": "[quote]"},
        {"id": ANY, "type": "p", "text": "Hello"},
        {
            "id": ANY,
            "type": "quote",
            "author": None,
            "post": None,
            "children": [
                {"id": ANY, "type": "p", "text": "world!"},
            ],
        },
    ]


@pytest.mark.asyncio
async def test_extra_closing_blocks_are_kept(context):
    result, _ = await parse_markup(context, "[quote]Hello [/quote]world![/quote]")
    assert result == [
        {
            "id": ANY,
            "type": "quote",
            "author": None,
            "post": None,
            "children": [{"id": ANY, "type": "p", "text": "Hello"}],
        },
        {"id": ANY, "type": "p", "text": "world!"},
        {"id": ANY, "type": "p", "text": "[/quote]"},
    ]


@pytest.mark.asyncio
async def test_interlocking_blocks_are_kept(context):
    result, _ = await parse_markup(
        context, "[quote]Lorem[spoiler]Ipsum[/quote]Dolor[/spoiler]"
    )
    assert result == [
        {
            "id": ANY,
            "type": "quote",
            "author": None,
            "post": None,
            "children": [
                {"id": ANY, "type": "p", "text": "Lorem"},
                {"id": ANY, "type": "p", "text": "[spoiler]"},
                {"id": ANY, "type": "p", "text": "Ipsum"},
            ],
        },
        {"id": ANY, "type": "p", "text": "Dolor"},
        {"id": ANY, "type": "p", "text": "[/spoiler]"},
    ]
