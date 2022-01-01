import pytest

from ..stats import aggregate_category_stats


@pytest.mark.asyncio
async def test_child_category_stats_are_added_to_parents(category, child_category):
    category = await category.update(threads=1, posts=2)
    child_category = await child_category.update(threads=3, posts=4)
    categories = aggregate_category_stats([category, child_category])

    assert categories[0].id == category.id
    assert categories[0].threads == category.threads + child_category.threads
    assert categories[0].posts == category.posts + child_category.posts

    assert categories[1].id == child_category.id
    assert categories[1].threads == child_category.threads
    assert categories[1].posts == child_category.posts
