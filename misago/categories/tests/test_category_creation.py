import pytest

from ..create import create_category
from ..get import get_category_by_id


@pytest.mark.asyncio
async def test_category_is_created_in_db(db):
    category = await create_category("test")
    assert category.id
    assert category == await get_category_by_id(category.id)


@pytest.mark.asyncio
async def test_category_is_created_with_slug(db):
    category = await create_category("TeST")
    assert category.slug == "test"


@pytest.mark.asyncio
async def test_category_is_created_without_mptt_data(db):
    category = await create_category("TeST")
    assert category.parent_id is None
    assert category.left == 0
    assert category.right == 0
    assert category.depth == 0


@pytest.mark.asyncio
async def test_category_is_created_with_parent_id(sibling_category):
    category = await create_category("TeST", parent=sibling_category)
    assert category.parent_id == sibling_category.id


@pytest.mark.asyncio
async def test_category_is_created_with_mptt_data(db):
    category = await create_category("TeST", left=1, right=2, depth=3)
    assert category.left == 1
    assert category.right == 2
    assert category.depth == 3
