=============
Notifications
=============


Modern site in which users interact with each other needs quick and efficient notifications system to let users know of each other actions as quickly as possible.

Misago implements such system and exposes simple as part of it, located in :py:mod:`misago.notifications`:


notify_user
-----------

.. function:: notify_user(user, message, url, trigger, formats=None, sender=None, update_user=True)

* ``user:`` User to notify.
* ``message:`` Notification message.
* ``url:`` Link user should follow to read message.
* ``trigger:`` short text used to identify this message for ``read_user_notification`` function.
* ``formats:`` Optional. Dict of formats for ``message`` argument that should be boldened.
* ``sender:`` Optional. User that notification origins from.
* ``update_user:``Optional. Boolean controlling if to call ``user.update`` after setting notification, or not.


read_user_notification
----------------------

.. function:: read_user_notification(user, trigger, atomic=True)

Sets user notification identified by ``trigger`` as read. This function checks internally if user has new notifications before it queries database.

* ``user:`` User to whom notification belongs to
* ``trigger:`` Short text used to identify messages to trigger as read.
* ``atomic:`` Lets you control if you should wrap this in dedicated transaction.
