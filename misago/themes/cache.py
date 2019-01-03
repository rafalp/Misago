from . import THEME_CACHE
from ..cache.versions import invalidate_cache


def clear_theme_cache():
    invalidate_cache(THEME_CACHE)
