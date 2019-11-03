import pytest

from ..versions import get_cache_versions


@pytest.mark.asyncio
async def test_getter_returns_cache_versions(db):
    cache_versions = await get_cache_versions()
    assert cache_versions.keys()
