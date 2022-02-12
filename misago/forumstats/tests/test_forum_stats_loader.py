import pytest

from ..loaders import load_forum_stats


@pytest.mark.asyncio
async def test_forum_stats_loader_loads_forum_stats(db):
    loaded_stats = await load_forum_stats({})
    assert loaded_stats


@pytest.mark.asyncio
async def test_forum_stats_loader_avoids_repeated_loads(db, mocker):
    context = {}
    get_forum_stats = mocker.patch(
        "misago.forumstats.loaders.get_forum_stats", return_value={"threads": 0}
    )
    await load_forum_stats(context)
    await load_forum_stats(context)
    get_forum_stats.assert_called_once()
