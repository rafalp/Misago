============
Cache Buster
============

Cache buster is small feature that allows certain cache-based systems find out when data they were dependant on has been changed, making their cache no longer valid.

Using Cache Buster
==================

Cache buster lives in :py:mod:`misago.core.cachebuster` and provides following API:


is_valid
--------

.. function:: is_valid(cache, version)

Checks if specific cache version is valid or raises ``ValueError`` if cache key is invalid.


get_version
-----------

.. function:: get_version(cache)

Returns current valid cache version as an integer number or raises ``ValueError`` if cache key is invalid.


invalidate
----------

.. function:: invalidate(cache)

Makes specified cache invalid.


invalidate_all
--------------

.. function:: invalidate_all()

Makes all versioned caches invalid.


Adding Custom Cache Buster
==========================

You may add and remove your own cache names to cache buster by using following commands:

.. note::
   Don't forget to call `invalidate_all` function after adding or removing cache name from buster to force it to rebuild its own cache.


register
--------

.. function:: register(cache)

Registers new cache in cache buster for tracking.


unregister
----------

.. function:: unregister(cache)

Removes cache from cache buster and disables its tracking. This function will raise ``ValueError`` if cache you are trying to unregister is not registered.
