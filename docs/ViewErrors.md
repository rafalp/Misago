View errors
===========

Modern forum software is busy place where access content is decided by many factors. This means that your users may frequently be trying to follow links that has been outdated, deleted or simply restricted and each of those scenarios must be handled by your views.

While Django provides [plenty of approaches](https://docs.djangoproject.com/en/{{ book.django_version }}/topics/http/views/#returning-errors>) to handling those situations, those can hardly be named fit for internet forum usecases. For example, you may want to communicate to your user a reason why he is not able to reply in selected thread at the moment. This brings need for custom error handling in your code.

And what to do if user reached page using outdated link? You will have to compare link to model's slug field and return 301 redirect to valid address on every view that has friendly link.

To solve this problem you would have to write custom error views and handlers that then you would have to add in every view that needs it. Depending on number of views you are writing, number of lines would quickly add up becoming annoying boilerplate.

Misago views too have to solve this problem and this reason is why error handling boilerplate is part of framework.


## Views Exceptions

While Misago raises plenty of exceptions, only four are allowed to leave views. Two of those are django's `Http404` and `PermissionDenied` exceptions. Misago defines its own two exceptions that act as "messages" for it's own error handler that link user followed to reach view is not up-to-date and could use 301 redirect to make sure bookmarks and crawlers get current link.


##### Note

You should never raise those exceptions yourself. If you want to redirect user to certain page, return proper redirect response instead.


### `misago.core.exceptions.Banned`

Raising this exception with `Ban` or `BanCache` instance as its only argument will cause Misago to display "You are banned" error page to the user.



### `misago.core.exceptions.ExplicitFirstPage`

This exception is raised by `misago.core.shortcuts.paginate` helper function that creates pagination for given data, page number and configuration. If first page is explicit (`user-blog/1/`) instead implicit (`user-blog/`), this exception is raised for error handler to return redirect to link with implicit first page.


##### Warning

This is reason why Misago views pass `None` as page number to `misago.core.shortcuts.paginate` when no page was passed through link.


### `misago.core.exceptions.OutdatedSlug`

This exception is raised by `misago.core.shortcuts.validate_slug` helper function that compares link's "slug" part against one from database. If check fails OutdatedSlug exception is raised with parameter name and valid slug as message that Misago's exception handler then uses to construct redirection response to valid link.


## The `misago.core.exceptionhandler` exception handler

Exception handler is lightweight system that pairs exceptions with special handling functions that turn those exceptions into valid HTTP responses that are then served back to client.

This system has been designed exlusively for handling exceptions listed in this document and is was not intended to be universal and extensible solution. If you need special handling for your own exception, depending on how wide is its usage, consider writing custom exception handler decorator or [middleware](https://docs.djangoproject.com/en/{{ book.django_version }}/topics/http/middleware/#process-exception) for it.
