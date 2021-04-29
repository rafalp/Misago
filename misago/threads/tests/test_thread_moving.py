import pytest

from ..move import move_thread, move_threads


@pytest.mark.asyncio
async def test_moving_thread_updates_its_category(thread, sibling_category):
    updated_thread = await move_thread(thread, sibling_category)
    assert updated_thread.category_id == sibling_category.id
    thread_from_db = await thread.refresh_from_db()
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
    post_from_db = await post.refresh_from_db()
    assert post_from_db.category_id == sibling_category.id


@pytest.mark.asyncio
async def test_moving_threads_updates_their_category(thread, sibling_category):
    updated_threads = await move_threads([thread], sibling_category)
    assert updated_threads[0].category_id == sibling_category.id
    thread_from_db = await thread.refresh_from_db()
    assert thread_from_db.category_id == sibling_category.id


@pytest.mark.asyncio
async def test_moving_threads_to_their_current_category_does_nothing(
    thread, category, mocker
):
    gather = mocker.patch("misago.threads.move.gather")
    updated_threads = await move_threads([thread], category)
    assert updated_threads[0] == thread
    gather.assert_not_called()


@pytest.mark.asyncio
async def test_moving_threads_moves_their_posts(thread, post, sibling_category):
    await move_threads([thread], sibling_category)
    post_from_db = await post.refresh_from_db()
    assert post_from_db.category_id == sibling_category.id
