from asyncio import gather
from typing import Dict

from ..database import database
from ..tables import cache_versions
from .utils import generate_version_string

CacheVersions = Dict[str, str]


async def get_cache_versions() -> CacheVersions:
    rows = await database.fetch_all(cache_versions.select(None))
    return {row["cache"]: row["version"] for row in rows}


async def invalidate_cache(cache: str) -> str:
    new_version = generate_version_string()
    query = (
        cache_versions.update(None)
        .values(version=new_version)
        .where(cache_versions.c.cache == cache)
    )
    await database.execute(query)
    return new_version


async def invalidate_all_caches() -> CacheVersions:
    new_versions = {}
    queries = []
    for cache in await get_cache_versions():
        new_versions[cache] = generate_version_string()
        queries.append(
            database.execute(
                cache_versions.update(None)
                .values(version=new_versions[cache])
                .where(cache_versions.c.cache == cache)
            )
        )
    await gather(*queries)
    return new_versions
