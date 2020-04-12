import pytest

from ..cache import FORUM_STATS_CACHE
from ..forumstats import get_forum_stats, get_forum_stats_from_db


@pytest.mark.asyncio
async def test_valid_forum_stats_are_retrieved_for_empty_forum(db):
    stats = await get_forum_stats_from_db()

    assert stats["threads"] == 0
    assert stats["posts"] == 0
    assert stats["users"] == 0


@pytest.mark.asyncio
async def test_valid_forum_stats_are_retrieved_for_forum_with_content(thread, user):
    stats = await get_forum_stats_from_db()

    assert stats["threads"] == 1
    assert stats["posts"] == 1
    assert stats["users"] == 1


@pytest.mark.asyncio
async def test_forum_stats_are_retrieved_with_id(db):
    stats = await get_forum_stats_from_db()
    assert stats["id"]


@pytest.mark.asyncio
async def test_forum_stats_are_retrieved_from_cache_if_it_exists(db, mocker):
    value = {"threads": 1}
    mocker.patch(
        "misago.forumstats.forumstats.get_forum_stats_cache", return_value=value
    )
    get_from_db = mocker.patch("misago.forumstats.forumstats.get_forum_stats_from_db")
    set_cache = mocker.patch("misago.forumstats.forumstats.set_forum_stats_cache")
    assert await get_forum_stats() == value
    get_from_db.assert_not_called()
    set_cache.assert_not_called()


@pytest.mark.asyncio
async def test_forum_stats_are_retrieved_from_db_and_cached_if_cache_doesnt_exists(
    db, mocker
):
    value = {"threads": 1}
    mocker.patch(
        "misago.forumstats.forumstats.get_forum_stats_cache", return_value=None
    )
    get_from_db = mocker.patch(
        "misago.forumstats.forumstats.get_forum_stats_from_db", return_value=value
    )
    set_cache = mocker.patch("misago.forumstats.forumstats.set_forum_stats_cache")
    assert await get_forum_stats() == value
    get_from_db.assert_called_once()
    set_cache.assert_called_once()
