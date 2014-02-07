=========================
Misago Shortcut Functions
=========================

Just like `Django <https://docs.djangoproject.com/en/dev/topics/http/shortcuts/>`_, Misago defines shortcuts module that reduce some procedures to single functions.

This module lives in :py:mod:`misago.views.shortcuts` and in addition to Misago-native shortcut functions, it imports whole of :py:mod:`django.shortcuts`, so you don't have to import it separately in your views.


validate_slug
-------------

.. function:: validate_slug(model, slug)

This function compares model instance's "slug" attribute against user-friendly slug that was passed as link parameter. If model's slug attribute is different this function, :py:class:`misago.views.OutdatedSlug` is raised. This exception is then captured by Misago's exception handler which makes Misago return permanent (http 301) redirect to client with valid link.

Example of view that first fetches object form database and then makes sure user or spider that reaches page has been let known of up-to-date link::


    from misago.views.shortcuts import validate_slug, get_object_or_404
    from myapp.models import Cake

    def cake_fans(request, cake_id, cake_slug):
        # first get cake model from DB
        cake = get_object_or_404(Cake, pk=cake_id)
        # issue redirect if cake slug is invalid
        validate_slug(cake, cacke_slug)


.. note::
   You may have noticed that there's no exception handling for either Http404 exception raised by ``get_object_or_404``, nor ``OutdatedSlug`` exception raised by ``validate_slug``. This is by design. Both exceptions are handled by Misago for you so you don't have to spend time writing exception handling boiler plate on every view that fetches objects from database and validates their links.

   Naturally if you need to, you can still handle them yourself.


.. note::
   Your links should use "slug" parameters only when they are supporting GET requests. For same reason you should call ``validate_slug`` only when request method is GET or HEAD.
