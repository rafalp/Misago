Cache
=====

Misago uses caching aggressivelly to save costful operations results like users ACLs resolution. Setting up cache, perfectly memory based one like Memcached is great way to speed up your forum and cut down database traffic.


## Setting up Misago-only cache

You can make Misago use its own cache instead of sharing cache with rest of your Django site. To do so, add new cache named `misago` to your `CACHES` setting:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'misago': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11212',
    }
}
```


## Cache buster

Cache buster is small feature that allows certain cache-based systems find out when data they were dependant on has been changed, making their cache no longer valid.

Cache buster lives in `misago.core.cachebuster` and provides following API:


#### `is_valid(cache_name, version)`

Checks if specific cache version is valid or raises ValueError if cache key is invalid.


#### `get_version(cache_name)`

Returns current valid cache version as an integer number or raises ValueError if cache key is invalid.


#### `invalidate(cache_name)`

Makes specified cache invalid.


#### `invalidate_all()`

Makes all versioned caches invalid.


### Example usage

Below snippet of code tests if cache version stored on `ban['version']` is current for bans cache:

```python
bans_cache_version = get_version('bans')
if not cachebuster.is_valid('bans', ban['version']):
    raise RuntimeError("ban was set before cache got invalidated and needs to be re-checked!")
```


### Adding Custom Cache Buster

You may add and remove your own cache names to cache buster by using following commands:


##### Note

Don't forget to call `invalidate_all` function after adding or removing cache name from buster to force it to rebuild its own cache.


#### `register(cache)`

Registers new cache in cache buster for tracking.


#### `unregister(cache)`

Removes cache from cache buster and disables its tracking. This function will raise `ValueError` if cache you are trying to unregister is not registered.


#### Registering cachebusters in migrations

Misago provides the `misago.core.migrationutils.cachebuster_unregister_cache(apps, cache)` utility command for setting cachebusters in migrations, like such:

```python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from misago.core.migrationutils import cachebuster_register_cache


def register_bans_version_tracker(apps, schema_editor):
    cachebuster_register_cache(apps, 'misago_bans')


class Migration(migrations.Migration):
    dependencies = [
        ('misago_core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(register_bans_version_tracker),
    ]

```