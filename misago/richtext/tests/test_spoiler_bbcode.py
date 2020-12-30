from unittest.mock import ANY

import pytest

from ..parser import parse_markup


@pytest.mark.asyncio
async def test_spoiler_bbcode_is_supported(graphql_context):
    result, _ = await parse_markup(graphql_context, "[spoiler]Hello world![/spoiler]")
    assert result == [
        {
            "id": ANY,
            "type": "spoiler",
            "children": [{"id": ANY, "type": "p", "text": "Hello world!"}],
        }
    ]
