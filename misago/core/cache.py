from django.core.cache import (InvalidCacheBackendError, get_cache,
                               cache as default_cache)


try:
    cache = get_cache('misago')
except InvalidCacheBackendError:
    cache = default_cache


try:
    fpc_cache = get_cache('misago_fpc')
except InvalidCacheBackendError:
    fpc_cache = cache
