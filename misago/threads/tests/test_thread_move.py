import pytest

from ..get import get_post_by_id, get_thread_by_id
from ..move import move_thread


@pytest.mark.asyncio
async def test_moving_thread_updates_its_category(thread, sibling_category):
    updated_thread = await move_thread(thread, sibling_category)
    assert updated_thread.category_id == sibling_category.id
    thread_from_db = await get_thread_by_id(thread.id)
    assert thread_from_db.category_id == sibling_category.id


@pytest.mark.asyncio
async def test_moving_thread_to_its_current_category_does_nothing(
    thread, category, mocker
):
    gather = mocker.patch("misago.threads.move.gather")
    updated_thread = await move_thread(thread, category)
    assert updated_thread == thread
    gather.assert_not_called()


@pytest.mark.asyncio
async def test_moving_thread_moves_its_posts(thread, post, sibling_category):
    await move_thread(thread, sibling_category)
    post_from_db = await get_post_by_id(post.id)
    assert post_from_db.category_id == sibling_category.id
