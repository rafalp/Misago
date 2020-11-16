from django.db.migrations import RunPython


class StartCacheVersioning(RunPython):
    def __init__(self, cache):
        code = start_cache_versioning(cache)
        reverse_code = stop_cache_versioning(cache)
        super().__init__(code, reverse_code)


class StopCacheVersioning(RunPython):
    def __init__(self, cache):
        code = stop_cache_versioning(cache)
        reverse_code = start_cache_versioning(cache)
        super().__init__(code, reverse_code)


def start_cache_versioning(cache):
    def migration_operation(apps, _):
        CacheVersion = apps.get_model("misago_cache", "CacheVersion")
        CacheVersion.objects.create(cache=cache)

    return migration_operation


def stop_cache_versioning(cache):
    def migration_operation(apps, _):
        CacheVersion = apps.get_model("misago_cache", "CacheVersion")
        CacheVersion.objects.filter(cache=cache).delete()

    return migration_operation
