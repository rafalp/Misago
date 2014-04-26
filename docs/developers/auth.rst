===================
User Authentication
===================


Admin Authentication
====================

Misago adds additional layer of security around admin areas in your site. This means that unless you've signed to admin area directly, you have to authenticate yourself one more time to upgrade your session from "casual" one to "administrator".

This mechanism was put in place because it's common for forum administrators to browse and use forums while signed on their administrator account. By default, Django requires user to be signed in and have special ``is_staff`` set on his or her account and know the path to administration backend to administrate site, which is good approach for situations when staff accounts are used exclusively for administration and not day to day usage.

In addition for re-authentication requirement, Misago also monitors inactivity periods between requests to admin interfaces, and if one exceeds length specified in ``MISAGO_ADMIN_SESSION_EXPIRATION`` setting, it will assume that administrator has been inactive and request another reauthentication upon next request to admin backend.

Implementation in this mechanism is placed within :py:mod:`misago.admin.auth` module and :py:class:`misago.admin.middleware.AdminAuthMiddleware` middleware. Middleware uses methods from ``auth`` to detect if request is pointed at protected namespace, and if it is, it uses facilities to handle and control state of administrators session.


.. function:: misago.admin.auth.is_admin_session(request)

Returns true if current request has valid administrator session. Otherwhise returns false.


.. function:: misago.admin.auth.start_admin_session(request, user)

Promotes current session to state of administrator session.


.. function:: misago.admin.auth.update_admin_session(request)

Updates last activity timestamp on admin session.


.. function:: misago.admin.auth.close_admin_session(request)

Closes current admin session, degrading it to "casual" session and keeps user signed in.


.. function:: login(request, user)

Signs user in just like Django :py:func:`django.contrib.auth.login` does and then promotes session to admin session.

.. function:: logout(request)

Signs user out just like Django :py:func:`django.contrib.auth.logout` does and terminates admin session.
