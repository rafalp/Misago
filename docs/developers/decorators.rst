================
Views Decorators
================

Misago apps define plenty of decorators for you to wrap your views with.


misago.core.decorators
======================


require_POST
------------

:py:func:`misago.core.decorators.require_POST`

Function that checks if request made to access view is POST. If it's not, decorator renders ''wrong_way.html'' template and returns it in 405-coded response. This is its only difference to Django's counterpart.


misago.core.errorpages
======================


shared_403_exception_handler
----------------------------

:py:func:`misago.core.errorpages.shared_403_exception_handler`

If your project has different error handler for 403 errors defined, you can use this decorator to make your function shared handler between Misago and other views. This will make Misago handle 403 exceptions coming from under its path while leaving alone exceptions coming from your site.


shared_404_exception_handler
----------------------------

:py:func:`misago.core.errorpages.shared_404_exception_handler`

Same as above but for custom 404 error handler.


misago.users.decorators
=======================


deny_authenticated
------------------

:py:func:`misago.users.decorators.deny_authenticated`

This decorator will block requests made to view if user is authenticated, displaying page with friendly error message in its stead.


deny_guests
-----------

:py:func:`misago.users.decorators.deny_guests`

This decorator will block requests made to view if user is not authenticated, displaying page with friendly error message in its stead.
