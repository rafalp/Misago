from ..cache.versions import get_cache_versions
from .dynamicsettings import DynamicSettings


def get_dynamic_settings():
    cache_versions = get_cache_versions()
    return DynamicSettings(cache_versions)
