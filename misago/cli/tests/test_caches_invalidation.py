import pytest
from asgiref.sync import sync_to_async

from ...cacheversions import get_cache_versions
from ...database.testing import existing_database_connection


@pytest.mark.asyncio
async def test_task_invalidates_caches(db, invoke_cli):
    cache_versions = await get_cache_versions()
    with existing_database_connection():
        await sync_to_async(invoke_cli)("invalidatecaches")
    updated_cache_versions = await get_cache_versions()
    assert updated_cache_versions != cache_versions
