========================
Views Errors Boilerplate
========================

Modern forum software is busy place where access content is decided by many factors. This means that your users may frequently be trying to follow links that has been outdated, deleted or simply restricted and each of those scenarios must be handled by your views.

While Django provides `plenty of approaches <https://docs.djangoproject.com/en/dev/topics/http/views/#returning-errors>`_ to handling those situations, those can hardly be named fit for internet forum usecases. For example, you may want to communicate to your user a reason why he is not able to reply in selected thread at the moment. This brings need for custom error handling in your code.

And what to do if user reached page using outdated link? You will have to compare link to model's slug field and return 301 redirect to valid address on every view that has friendly link.

To solve this problem you would have to write custom error views and handlers that then you would have to add in every view that needs it. Depending on number of views you are writing, number of lines would quickly add up becoming annoying boilerplate.

Misago views too have to solve this problem and this reason is why error handling boilerplate is part of framework.


Http404
=======

:py:class:`misago.views.exceptions.Http404`

Misago's Http404 exception subclasses `Django Http404 <https://docs.djangoproject.com/en/dev/topics/http/views/#the-http404-exception>`_, but changes nothing about its implementation and exists simply to delegate 404 error handling to Misago's exceptions handler.

Raise this exception if requested page does not exists or user's permission set shows that he shouldn't know if it exists. If you want to, you can insert custom error message into exception's constructor to be displayed by error page instead of default one.


   raise Http404("Requested thread could not be found. Perhaps it was moved or deleted?")


OutdatedUrl
===========

:py:class:`misago.views.exceptions.OutdatedUrl`

OutdatedUrl exception is special "message" that tells Misago to return `permanent <http://en.wikipedia.org/wiki/HTTP_301>`_ redirection as response instead of intended view.

This exception is raised by view utility that compares link's "slug" part against one from database. If check fails OutdatedUrl exception is raised with parameter name and valid slug as message that Misago's exception handler then uses to construct redirection response to valid link.

You should never raise this exception yourself, instead always return proper redirect response from your code.


PermissionDenied
================

:py:class:`misago.views.exceptions.PermissionDenied`

Misago's PermissionDenied exception subclasses `Django PermissionDenied <https://docs.djangoproject.com/en/dev/ref/exceptions/#django.core.exceptions.PermissionDenied>`_, but changes nothing about its implementation and exists simply to delegate 403 error handling to Misago's exceptions handler.

Raise this exception if user knows of requested page or action but has no permission to access or perform it. If you want to, you can insert custom error message into exception's constructor to be displayed by error page instead of default one.

    raise PermissionDenied("This thread is locked. You can't reply to it.")


Exception Handler
=================

:py:mod:`misago.views.exceptions.handler`

Exception handler is lightweight system that pairs exceptions with special "handler" functions that turn those exceptions into valid HTTP responses that are then served back to client.

This system has been designed exlusively for handling exceptions listed in this document and is was not intended to be universal and extensible solution. If you need special handling for your own exception, depending on how wide is its usage, consider writing custom exception handler decorator or `middleware <https://docs.djangoproject.com/en/dev/topics/http/middleware/#process-exception>`_ for it.
