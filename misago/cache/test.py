from .versions import get_cache_versions_from_db


class assert_invalidates_cache:
    def __init__(self, cache):
        self.cache = cache

    def __enter__(self):
        self.versions = get_cache_versions_from_db()
        return self

    def __exit__(self, *_):
        new_versions = get_cache_versions_from_db()
        for cache, version in new_versions.items():
            if cache == self.cache:
                message = "cache %s was not invalidated" % cache
                assert self.versions[cache] != version, message
        
