=============
Notifications
=============

Modern site in which users interact with each other needs quick and efficient notifications system to let users know of each other actions as quickly as possible.

Misago implements such system and exposes simple as part of it, located in :py:mod:`misago.notifications`:


notify_user
-----------

.. function:: notify_user(user, message, url, type, formats=None, sender=None, update_user=True)

* ``user:`` User to notify.
* ``message:`` Notification message.
* ``url:`` Link user should follow to read message.
* ``type:`` short text used to identify this message for ``read_user_notifications`` function. For example ``see_thread_123`` notification will be read when user sees thread with ID 123 for first time.
* ``formats:`` Optional. Dict of formats for ``message`` argument that should be boldened.
* ``sender:`` Optional. User that notification origins from.
* ``update_user:`` Optional. Boolean controlling if to call ``user.update`` after setting notification, or not. Defaults to ``True``.


read_user_notifications
-----------------------

.. function:: read_user_notifications(user, types, atomic=True)

Sets user notifications identified by ``types`` as read. This function checks internally if user has new notifications before it queries database.

* ``user:`` User to whom notification belongs to
* ``types:`` Short text or list of short texts used to identify notifications that will be set as read.
* ``atomic:`` Lets you control if you should wrap this in dedicated transaction.
