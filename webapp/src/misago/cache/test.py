from .versions import get_cache_versions


class assert_invalidates_cache:
    def __init__(self, cache):
        self.cache = cache

    def __enter__(self):
        self.versions = get_cache_versions()
        return self

    def __exit__(self, exc_type, *_):
        if exc_type:
            return False

        new_versions = get_cache_versions()
        for cache, version in new_versions.items():
            if cache == self.cache:
                message = "cache %s was not invalidated" % cache
                assert self.versions[cache] != version, message
