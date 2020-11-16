from .versions import get_cache_versions


def cache_versions_middleware(get_response):
    """Sets request.cache_versions attribute with dict of cache versions."""

    def middleware(request):
        request.cache_versions = get_cache_versions()
        return get_response(request)

    return middleware
