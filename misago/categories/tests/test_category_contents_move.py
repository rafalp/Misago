import pytest

from ..contents import move_categories_contents


@pytest.mark.asyncio
async def test_category_threads_and_posts_are_moved(
    category, sibling_category, thread, post
):
    assert thread.category_id == category.id
    assert post.category_id == category.id

    await move_categories_contents([category], sibling_category)

    updated_thread = await thread.fetch_from_db()
    assert updated_thread.category_id == sibling_category.id

    updated_post = await post.fetch_from_db()
    assert updated_post.category_id == sibling_category.id


@pytest.mark.asyncio
async def test_other_categories_threads_and_posts_are_excluded_from_move(
    category,
    sibling_category,
    closed_category,
    closed_category_thread,
    closed_category_post,
):
    assert closed_category_thread.category_id == closed_category.id
    assert closed_category_post.category_id == closed_category.id

    await move_categories_contents([category], sibling_category)

    updated_thread = await closed_category_thread.fetch_from_db()
    assert updated_thread.category_id == closed_category.id

    updated_post = await closed_category_post.fetch_from_db()
    assert updated_post.category_id == closed_category.id
