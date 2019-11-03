import pytest

from ..versions import get_cache_versions, invalidate_all_caches, invalidate_cache


@pytest.mark.asyncio
async def test_invalidating_cache_updates_cache_version_in_database(cache_version):
    await invalidate_cache(cache_version["cache"])
    updated_cache_versions = await get_cache_versions()
    assert cache_version["version"] != updated_cache_versions[cache_version["cache"]]


@pytest.mark.asyncio
async def test_invalidating_all_caches_updates_cache_version_in_database(cache_version):
    new_cache_versions = await invalidate_all_caches()
    updated_cache_versions = await get_cache_versions()
    assert cache_version["version"] != updated_cache_versions[cache_version["cache"]]
    assert updated_cache_versions == new_cache_versions
