from caches import Cache

from .conf import settings

cache = Cache(settings.cache_url, force_rollback=settings.test)
