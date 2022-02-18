from unittest.mock import ANY

import pytest

from ..parser import parse_markup


@pytest.mark.asyncio
async def test_horizontal_line_bbcode_is_supported(context):
    result, _ = await parse_markup(context, "Hello\n\n[hr]\n\nWorld")
    assert result == [
        {
            "id": ANY,
            "type": "p",
            "text": "Hello",
        },
        {
            "id": ANY,
            "type": "hr",
        },
        {
            "id": ANY,
            "type": "p",
            "text": "World",
        },
    ]
