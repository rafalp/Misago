import pytest

from ..threads import load_threads_feed


@pytest.mark.asyncio
async def test_threads_feed_loader_returns_feed_with_threads(graphql_context, thread):
    loaded_feed = await load_threads_feed(graphql_context)
    assert loaded_feed.items == [thread]


@pytest.mark.asyncio
async def test_threads_feed_loader_returns_feed_with_threads_after_cursor(
    graphql_context, thread, user_thread
):
    loaded_feed = await load_threads_feed(
        graphql_context, cursor=str(user_thread.last_post_id)
    )
    assert loaded_feed.items == [thread]


@pytest.mark.asyncio
async def test_threads_feed_loader_returns_none_if_cursor_is_invalid(
    graphql_context, thread
):
    loaded_feed = await load_threads_feed(graphql_context, cursor="invalid")
    assert loaded_feed is None


@pytest.mark.asyncio
async def test_threads_feed_loader_returns_feed_with_user_threads(
    graphql_context, thread, user_thread, user
):
    loaded_feed = await load_threads_feed(graphql_context, starter_id=str(user.id))
    assert loaded_feed.items == [user_thread]


@pytest.mark.asyncio
async def test_threads_feed_loader_returns_empty_feed_if_starter_id_is_invalid(
    graphql_context, thread
):
    loaded_feed = await load_threads_feed(graphql_context, starter_id="invalid")
    assert loaded_feed is None


@pytest.mark.asyncio
async def test_threads_feed_loader_returns_feed_with_threads_in_category(
    graphql_context, thread, category, closed_category_thread
):
    loaded_feed = await load_threads_feed(graphql_context, categories=[category])
    assert loaded_feed.items == [thread]


@pytest.mark.asyncio
async def test_threads_feed_loader_returns_empty_feed_if_categories_list_is_empty(
    graphql_context, thread
):
    loaded_feed = await load_threads_feed(graphql_context, categories=[])
    assert loaded_feed.items == []
