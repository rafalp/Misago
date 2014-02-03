==================
Context Processors
==================

Context Processors are simple python functions that receive HttpRequest object and extend template context with additional values. In addition to `default context processors defined by Django <https://docs.djangoproject.com/en/dev/ref/templates/api/#subclassing-context-requestcontext>`_, Misago defines its own context processors:


misago.core.context_processors.site_address
===========================================

:py:func:`misago.core.context_processors.site_address`

This function adds ``SITE_ADDRESS`` value to template context that you can use to build absolue links in your templates::

    # Will become "http://mysite.com/"
    {{ SITE_ADDRESS }}{% url 'forum_index' %}

This is most useful for links in e-mail templates.
