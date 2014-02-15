from django.core.cache import InvalidCacheBackendError, get_cache


try:
    cache = get_cache('misago')
except InvalidCacheBackendError:
    cache = get_cache('default')


try:
    fpc_cache = get_cache('misago_fpc')
except InvalidCacheBackendError:
    fpc_cache = cache
