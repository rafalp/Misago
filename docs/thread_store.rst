===================
Misago Thread Store
===================

Thread store is simple memory-based cache some Misago features use to maintain state for request duration.

.. warning::
   :py:mod:`misago.core.threadstore` is considered part of internals and generally should be avoided unless

It offers subset of standard cache API:


get
---

.. function:: get(key[, default=None])

Get value for key from thread store or default value if key is undefined.

    >>> from misago.core import threadstore
	>>> get('peach')
	None

	>>> get('peach', 'no peach!')
	'no peach!'


get() never raises an exception for non-existant value which is why you should avoid storing "None" values and use custom default values to spot non-existant keys.


set
---

.. function:: set(key, value)

Set value for a key on thread store. This value will then be stored until you overwrite it with new value, thread is killed, :py:mod:`misago.core.middleware.ThreadStoreMiddleware` process_response method is called, or you explictly call clear() funciton, clearing thread store.


clear
-----

.. function:: clear()

Delete all values from thread store. This function is automatically called by ThreadStoreMiddleware to make sure contents of thread store won't have effect on next request.
