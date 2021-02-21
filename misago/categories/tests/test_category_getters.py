import pytest

from ..get import get_all_categories, get_category_by_id
from ..update import update_category


@pytest.mark.asyncio
async def test_categories_list_can_be_get(categories):
    assert await get_all_categories()


@pytest.mark.asyncio
async def test_category_can_be_get_by_id(category):
    assert category == await get_category_by_id(category.id)


@pytest.mark.asyncio
async def test_getting_category_by_nonexistent_id_returns_none(db):
    assert await get_category_by_id(2000) is None


@pytest.mark.asyncio
@pytest.mark.xfail(reason="stat aggregation removed for now")
async def test_child_categories_stats_are_added_to_parent_stats(
    category, child_category
):
    await update_category(child_category, threads=10, posts=20)
    categories = await get_all_categories()
    assert categories[category.id].threads == 10
    assert categories[category.id].posts == 20
