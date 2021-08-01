import pytest

from ..get import get_category_by_id
from ..models import Category


@pytest.mark.asyncio
async def test_category_is_created_in_db(db):
    category = await Category.create("test")
    assert category.id
    assert category == await get_category_by_id(category.id)


@pytest.mark.asyncio
async def test_category_is_created_with_slug(db):
    category = await Category.create("TeST")
    assert category.slug == "test"


@pytest.mark.asyncio
async def test_category_is_created_with_default_color(db):
    category = await Category.create("Test")
    assert len(category.color) == 4
    assert category.color[0] == "#"


@pytest.mark.asyncio
async def test_category_is_created_with_custom_color(db):
    category = await Category.create("Test", color="#ff0000")
    assert category.color == "#FF0000"


@pytest.mark.asyncio
async def test_category_is_created_without_custom_icon(db):
    category = await Category.create("Test")
    assert category.icon is None


@pytest.mark.asyncio
async def test_category_is_created_with_custom_icon(db):
    category = await Category.create("Test", icon="icon")
    assert category.icon == "icon"


@pytest.mark.asyncio
async def test_category_is_created_without_mptt_data(db):
    category = await Category.create("TeST")
    assert category.parent_id is None
    assert category.left == 0
    assert category.right == 0
    assert category.depth == 0


@pytest.mark.asyncio
async def test_category_is_created_with_parent_id(sibling_category):
    category = await Category.create("TeST", parent=sibling_category)
    assert category.parent_id == sibling_category.id


@pytest.mark.asyncio
async def test_category_is_created_with_mptt_data(db):
    category = await Category.create("TeST", left=1, right=2, depth=3)
    assert category.left == 1
    assert category.right == 2
    assert category.depth == 3


@pytest.mark.asyncio
async def test_category_is_created_open(db):
    category = await Category.create("TeST")
    assert not category.is_closed


@pytest.mark.asyncio
async def test_category_is_created_closed(db):
    category = await Category.create("TeST", is_closed=True)
    assert category.is_closed
