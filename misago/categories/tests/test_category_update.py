from dataclasses import replace

import pytest

from ..models import Category


@pytest.fixture
async def category(category):
    return await Category.create("Test category", icon="icon")


@pytest.mark.asyncio
async def test_category_name_is_updated(category):
    updated_category = await category.update(name="New name")
    assert updated_category.name == "New name"
    assert updated_category.slug == "new-name"


@pytest.mark.asyncio
async def test_category_color_is_updated(category):
    updated_category = await category.update(color="#0000ff")
    assert updated_category.color == "#0000FF"


@pytest.mark.asyncio
async def test_category_icon_is_updated(category):
    updated_category = await category.update(icon="new-icon")
    assert updated_category.icon == "new-icon"


@pytest.mark.asyncio
async def test_category_icon_can_be_removed(category):
    updated_category = await category.update(icon="")
    assert updated_category.icon is None


@pytest.mark.asyncio
async def test_category_parent_is_updated(category, sibling_category):
    updated_category = await category.update(parent=sibling_category)
    assert updated_category.parent_id == sibling_category.id


@pytest.mark.asyncio
async def test_category_parent_is_not_removed_if_new_value_is_none(category):
    category = replace(category, parent_id=1)
    updated_category = await category.update(parent=None)
    assert updated_category.parent_id == 1


@pytest.mark.asyncio
async def test_category_parent_can_be_removed(category):
    category = replace(category, parent_id=1)
    updated_category = await category.update(parent=False)
    assert updated_category.parent_id is None


@pytest.mark.asyncio
async def test_changing_parent_category_to_true_raises_error(category):
    with pytest.raises(ValueError):
        await category.update(parent=True)


@pytest.mark.asyncio
async def test_category_left_is_updated(category):
    updated_category = await category.update(left=42)
    assert updated_category.left == 42


@pytest.mark.asyncio
async def test_category_right_is_updated(category):
    updated_category = await category.update(right=42)
    assert updated_category.right == 42


@pytest.mark.asyncio
async def test_category_depth_is_updated(category):
    updated_category = await category.update(depth=42)
    assert updated_category.depth == 42


@pytest.mark.asyncio
async def test_category_threads_count_is_updated(category):
    updated_category = await category.update(threads=42)
    assert updated_category.threads == 42


@pytest.mark.asyncio
async def test_category_threads_count_can_be_incremented(category):
    updated_category = await category.update(increment_threads=True)
    assert updated_category.threads == 1


@pytest.mark.asyncio
async def test_updating_and_incrementing_category_threads_count_at_same_time_errors(
    category,
):
    with pytest.raises(ValueError):
        await category.update(threads=42, increment_threads=True)


@pytest.mark.asyncio
async def test_category_posts_count_is_updated(category):
    updated_category = await category.update(posts=42)
    assert updated_category.posts == 42


@pytest.mark.asyncio
async def test_category_posts_count_can_be_incremented(category):
    updated_category = await category.update(increment_posts=True)
    assert updated_category.posts == 1


@pytest.mark.asyncio
async def test_updating_and_incrementing_category_posts_count_at_same_time_errors(
    category,
):
    with pytest.raises(ValueError):
        await category.update(posts=42, increment_posts=True)


@pytest.mark.asyncio
async def test_open_category_can_be_closed(category):
    updated_category = await category.update(is_closed=True)
    assert updated_category.is_closed


@pytest.mark.asyncio
async def test_closed_category_can_be_opened(category):
    category = replace(category, is_closed=True)
    updated_category = await category.update(is_closed=False)
    assert not updated_category.is_closed


@pytest.mark.asyncio
async def test_category_extra_is_updated(category):
    extra = {"new": True}
    updated_category = await category.update(extra=extra)
    assert updated_category.extra == extra
