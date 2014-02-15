=============
Misago Caches
=============

You can make Misago use its own cache instead of sharing cache with rest of your Django site. To do so, add new cache named ``misago`` to your ``CACHES`` setting::

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


Full-Page Cache
---------------

By default Full-Page Cache ("FPC") uses same cache other Misago features do, however on active site this may cause your cache backend to frequently delete other still valid caches if it runs out of space.

To avert this, you can define one more cache named ``misago_fpc``.
