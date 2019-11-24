import pytest

from ...cacheversions import invalidate_cache
from ..cacheversions import assert_invalidates_cache


@pytest.mark.asyncio
async def test_assertion_fails_if_specified_cache_is_not_invalidated(cache_version):
    with pytest.raises(AssertionError):
        async with assert_invalidates_cache(cache_version["cache"]):
            pass


@pytest.mark.asyncio
async def test_assertion_passess_if_specified_cache_is_invalidated(cache_version):
    async with assert_invalidates_cache(cache_version["cache"]):
        await invalidate_cache(cache_version["cache"])


@pytest.mark.asyncio
async def test_assertion_fails_if_other_cache_is_invalidated(
    cache_version, other_cache_version
):
    with pytest.raises(AssertionError):
        async with assert_invalidates_cache(cache_version["cache"]):
            await invalidate_cache(other_cache_version["cache"])
