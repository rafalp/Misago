from dataclasses import replace

import pytest

from ..create import create_category
from ..update import update_category


@pytest.fixture
async def category(category):
    return await create_category("Test category")


@pytest.mark.asyncio
async def test_category_name_can_be_updated(category):
    updated_category = await update_category(category, name="New name")
    assert updated_category.name == "New name"
    assert updated_category.slug == "new-name"


@pytest.mark.asyncio
async def test_category_parent_can_be_updated(category, sibling_category):
    updated_category = await update_category(category, parent=sibling_category)
    assert updated_category.parent_id == sibling_category.id


@pytest.mark.asyncio
async def test_category_parent_is_not_removed_if_new_value_is_none(category):
    category = replace(category, parent_id=1)
    updated_category = await update_category(category, parent=None)
    assert updated_category.parent_id == 1


@pytest.mark.asyncio
async def test_category_parent_can_be_removed(category):
    category = replace(category, parent_id=1)
    updated_category = await update_category(category, parent=False)
    assert updated_category.parent_id is None


@pytest.mark.asyncio
async def test_changing_parent_category_to_true_raises_error(category):
    with pytest.raises(ValueError):
        await update_category(category, parent=True)


@pytest.mark.asyncio
async def test_category_left_can_be_updated(category):
    updated_category = await update_category(category, left=42)
    assert updated_category.left == 42


@pytest.mark.asyncio
async def test_category_right_can_be_updated(category):
    updated_category = await update_category(category, right=42)
    assert updated_category.right == 42


@pytest.mark.asyncio
async def test_category_depth_can_be_updated(category):
    updated_category = await update_category(category, depth=42)
    assert updated_category.depth == 42


@pytest.mark.asyncio
async def test_category_threads_count_can_be_updated(category):
    updated_category = await update_category(category, threads=42)
    assert updated_category.threads == 42


@pytest.mark.asyncio
async def test_category_threads_count_can_be_incremented(category):
    updated_category = await update_category(category, increment_threads=True)
    assert updated_category.threads == 1


@pytest.mark.asyncio
async def test_updating_and_incrementing_category_threads_count_at_same_time_errors(
    category,
):
    with pytest.raises(ValueError):
        await update_category(category, threads=42, increment_threads=True)


@pytest.mark.asyncio
async def test_category_posts_count_can_be_updated(category):
    updated_category = await update_category(category, posts=42)
    assert updated_category.posts == 42


@pytest.mark.asyncio
async def test_category_posts_count_can_be_incremented(category):
    updated_category = await update_category(category, increment_posts=True)
    assert updated_category.posts == 1


@pytest.mark.asyncio
async def test_updating_and_incrementing_category_posts_count_at_same_time_errors(
    category,
):
    with pytest.raises(ValueError):
        await update_category(category, posts=42, increment_posts=True)


@pytest.mark.asyncio
async def test_open_category_can_be_closed(category):
    updated_category = await update_category(category, is_closed=True)
    assert updated_category.is_closed


@pytest.mark.asyncio
async def test_closed_category_can_be_opened(category):
    category = replace(category, is_closed=True)
    updated_category = await update_category(category, is_closed=False)
    assert not updated_category.is_closed


@pytest.mark.asyncio
async def test_category_extra_can_be_updated(category):
    extra = {"new": True}
    updated_category = await update_category(category, extra=extra)
    assert updated_category.extra == extra
