=================
Misago Exceptions
=================

In addition to exceptions defined by `Django <https://docs.djangoproject.com/en/dev/ref/exceptions/>`_ and standard Python exceptions, Misago raises its own exceptions.

All Misago exceptions can be found in :py:mod:`misago.core.exceptions`.


PermissionDenied
----------------

Misago's Http404 exception subclasses `Django PermissionDenied <https://docs.djangoproject.com/en/dev/ref/exceptions/#django.core.exceptions.PermissionDenied>`_, but changes nothing about its implementation and exists simply to delegate 403 error handling to Misago's exceptions handler.


Http404
-------

Misago's Http404 exception subclasses `Django Http404 <https://docs.djangoproject.com/en/dev/topics/http/views/#the-http404-exception>`_, but changes nothing about its implementation and exists simply to delegate 404 error handling to Misago's exceptions handler.


OutdatedUrl
------------

OutdatedLink exception is special "message" that tells Misago to return `permanent <http://en.wikipedia.org/wiki/HTTP_301>`_ redirection as response instead of intended view.

This exception is raised by view utility that compares link's "slug" part against one from database. If check fails OutdatedLink exception is raised with parameter name and valid slug as message that Misago's exception handler then uses to construct redirection response to valid link.

You should never raise this exception yourself, instead always return proper redirect response from your code.
