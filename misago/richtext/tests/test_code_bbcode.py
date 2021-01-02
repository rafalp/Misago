from unittest.mock import ANY

import pytest

from ..parser import parse_markup


@pytest.mark.asyncio
async def test_code_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "[code]Hello **world**![/code]")
    assert result == [
        {"id": ANY, "type": "code", "syntax": None, "text": "Hello **world**!"}
    ]


@pytest.mark.asyncio
async def test_code_bbcode_with_syntax_is_supported(graphql_context):
    result, _ = await parse_markup(
        graphql_context, "[code=python]Hello **world**![/code]"
    )
    assert result == [
        {"id": ANY, "type": "code", "syntax": "python", "text": "Hello **world**!"}
    ]


@pytest.mark.asyncio
async def test_code_bbcode_works_for_other_bbcode(graphql_context):
    result, _ = await parse_markup(
        graphql_context, "[code=python][quote]Hello world![/quote][/code]"
    )
    assert result == [
        {
            "id": ANY,
            "type": "code",
            "syntax": "python",
            "text": "[quote]Hello world![/quote]",
        }
    ]
