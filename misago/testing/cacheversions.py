from typing import Dict

from ..cacheversions import get_cache_versions


class assert_invalidates_cache:
    _cache: str
    _versions: Dict[str, str]

    def __init__(self, cache: str):
        self._cache = cache

    async def __aenter__(self):
        self._versions = await get_cache_versions()
        return self

    async def __aexit__(self, exc_type: BaseException, *_):
        if exc_type:
            return False

        new_versions = await get_cache_versions()
        for cache, version in new_versions.items():
            if cache == self._cache:
                message = f"cache {cache} was not invalidated"
                assert self._versions[cache] != version, message
