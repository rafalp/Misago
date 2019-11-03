from asyncio import gather
from typing import Dict

from ..database import database
from ..database.queries import fetch_all
from ..tables import cache_versions
from .utils import generate_version_string


async def get_cache_versions() -> Dict[str, str]:
    return {i["cache"]: i["version"] for i in await fetch_all(cache_versions)}


async def invalidate_cache(cache: str) -> str:
    new_version = generate_version_string()
    query = (
        cache_versions.update(None)
        .values(version=new_version)
        .where(cache_versions.c.cache == cache)
    )
    await database.execute(query)
    return new_version


async def invalidate_all_caches() -> Dict[str, str]:
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
