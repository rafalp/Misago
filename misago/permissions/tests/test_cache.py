import pytest
import pytest_asyncio
from caches import Cache

from ...testing import assert_invalidates_cache
from ..cache import (
    MODERATORS_CACHE,
    PERMISSIONS_CACHE,
    clear_moderators_cache,
    clear_permissions_cache,
    get_moderators_cache,
    get_permissions_cache,
    set_moderators_cache,
    set_permissions_cache,
)

PERMS_ID = "perms_id"


@pytest_asyncio.fixture
async def cache(mocker):
    async with Cache("locmem://test") as c:
        mocker.patch("misago.permissions.cache.cache", c)
        yield c


@pytest.mark.asyncio
async def test_permissions_are_cached_and_returned(cache, cache_versions):
    perms = {"core": "TEST"}
    await set_permissions_cache(cache_versions, PERMS_ID, perms)
    cached_perms = await get_permissions_cache(cache_versions, PERMS_ID)
    assert cached_perms == perms


@pytest.mark.asyncio
async def test_expired_permissions_cache_is_not_returned(cache, cache_versions):
    perms = {"core": "TEST"}
    await set_permissions_cache(cache_versions, PERMS_ID, perms)
    cache_versions[PERMISSIONS_CACHE] = "new"
    cached_perms = await get_permissions_cache(cache_versions, PERMS_ID)
    assert cached_perms is None


@pytest.mark.asyncio
async def test_empty_permissions_cache_is_returned(cache, cache_versions):
    cached_perms = await get_permissions_cache(cache_versions, PERMS_ID)
    assert cached_perms is None


@pytest.mark.asyncio
async def test_permissions_cache_is_cleared(db):
    async with assert_invalidates_cache(PERMISSIONS_CACHE):
        await clear_permissions_cache()


@pytest.mark.asyncio
async def test_moderators_are_cached_and_returned(cache, cache_versions):
    moderators = {123: ([1], [3])}
    await set_moderators_cache(cache_versions, moderators)
    cached_moderators = await get_moderators_cache(cache_versions)
    assert cached_moderators == moderators


@pytest.mark.asyncio
async def test_expired_moderators_cache_is_not_returned(cache, cache_versions):
    moderators = {123: ([1], [3])}
    await set_moderators_cache(cache_versions, moderators)
    cache_versions[MODERATORS_CACHE] = "new"
    cached_moderators = await get_moderators_cache(cache_versions)
    assert cached_moderators is None


@pytest.mark.asyncio
async def test_empty_moderators_cache_is_returned(cache, cache_versions):
    cached_moderators = await get_moderators_cache(cache_versions)
    assert cached_moderators is None


@pytest.mark.asyncio
async def test_moderators_cache_is_cleared(db):
    async with assert_invalidates_cache(MODERATORS_CACHE):
        await clear_moderators_cache()
