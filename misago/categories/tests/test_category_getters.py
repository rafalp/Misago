import pytest

from ..get import get_all_categories


@pytest.mark.asyncio
async def test_categories_list_can_be_get():
    assert await get_all_categories()
