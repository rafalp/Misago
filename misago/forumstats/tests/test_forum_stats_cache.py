import pytest

from ..cache import (
    CACHE_TIMEOUT,
    FORUM_STATS_CACHE,
    clear_forum_stats_cache,
    get_forum_stats_cache,
    set_forum_stats_cache,
)


value = {"threads": 123}


@pytest.mark.asyncio
async def test_forum_stats_can_be_cached(mocker):
    set_cache = mocker.patch("misago.forumstats.cache.cache.set")
    await set_forum_stats_cache(value)
    set_cache.assert_called_once_with(FORUM_STATS_CACHE, value, ttl=CACHE_TIMEOUT)


@pytest.mark.asyncio
async def test_forum_stats_can_be_retrieved_from_cache(mocker):
    get_cache = mocker.patch("misago.forumstats.cache.cache.get", return_value=value)
    assert await get_forum_stats_cache() == value
    get_cache.assert_called_once_with(FORUM_STATS_CACHE)


@pytest.mark.asyncio
async def test_forum_stats_cache_can_be_cleared(mocker):
    clear_cache = mocker.patch("misago.forumstats.cache.cache.delete")
    await clear_forum_stats_cache()
    clear_cache.assert_called_once_with(FORUM_STATS_CACHE)
