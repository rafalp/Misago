from unittest.mock import ANY

import pytest


RICH_TEXT_QUERY = """
    query Search($markup: String!) {
        richText(markup: $markup)
    }
"""


@pytest.mark.asyncio
async def test_rich_text_query_resolves_to_parsed_markup(query_public_api, db):
    result = await query_public_api(RICH_TEXT_QUERY, {"markup": "Hello world!"})
    assert result["data"]["richText"] == [
        {"id": ANY, "type": "p", "text": "Hello world!"},
    ]
