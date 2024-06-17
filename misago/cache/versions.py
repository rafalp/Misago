from .models import CacheVersion
from .utils import generate_version_string


def get_cache_versions() -> dict[str, str]:
    queryset = CacheVersion.objects.all()
    return {i.cache: i.version for i in queryset}


def invalidate_cache(*cache_name: str) -> None:
    CacheVersion.objects.filter(cache__in=cache_name).update(
        version=generate_version_string()
    )


def invalidate_all_caches() -> None:
    for cache_name in get_cache_versions().keys():
        CacheVersion.objects.filter(cache=cache_name).update(
            version=generate_version_string()
        )
