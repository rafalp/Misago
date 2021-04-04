import pytest

from ..get import get_category_by_id
from ..sync import sync_category


@pytest.mark.asyncio
async def test_category_sync_updates_threads_count(category, thread):
    assert category.threads == 0

    updated_category = await sync_category(category)
    assert updated_category.threads == 1

    category_from_db = await get_category_by_id(category.id)
    assert category_from_db.threads == 1


@pytest.mark.asyncio
async def test_category_sync_updates_posts_count(category, thread):
    assert category.posts == 0

    updated_category = await sync_category(category)
    assert updated_category.posts == 1

    category_from_db = await get_category_by_id(category.id)
    assert category_from_db.posts == 1
