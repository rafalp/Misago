from django.core.cache import (caches, cache as default_cache,
                               InvalidCacheBackendError)


try:
    cache = caches['misago']
except InvalidCacheBackendError:
    cache = default_cache


try:
    fpc_cache = caches['misago_fpc']
except InvalidCacheBackendError:
    fpc_cache = cache
