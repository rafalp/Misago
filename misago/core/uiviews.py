"""
Misago UI views controller

UI views are small views that are called asynchronically to give UI knowledge
of changes in APP state and thus opportunity to update themselves in real time
"""
from time import time

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import resolve
from django.http import Http404, JsonResponse

from misago.users.online.tracker import mute_tracker

from misago.core.decorators import ajax_only
from misago.core.utils import is_referer_local


__all__ = ['uiview', 'uiserver']


UI_VIEWS = []


def uiview(name, cache_frequency=15):
    """
    Decorator for registering UI views
    """
    def namespace_decorator(f):
        UI_VIEWS.append((name, cache_frequency, f))
        return f
    return namespace_decorator


def get_resolver_match(request):
    requesting_path = request.META['HTTP_REFERER']
    requesting_path = requesting_path[len(request.scheme) + 3:]
    requesting_path = requesting_path[len(request.META['HTTP_HOST']):]

    try:
        return resolve(requesting_path)
    except Http404:
        return None


@ajax_only
def uiserver(request):
    mute_tracker(request)

    if not is_referer_local(request):
        raise PermissionDenied()

    resolver_match = get_resolver_match(request)
    response_dict = {}

    now = int(time())

    for name, cache_frequency, view in UI_VIEWS:
        cache_key = 'uijson_%s' % name
        cache = request.session.get(cache_key)

        if not cache or cache['expires'] < now:
            try:
                view_response = view(request, resolver_match)
            except PermissionDenied:
                view_response = None

            request.session[cache_key] = {
                'json': view_response,
                'expires': now + cache_frequency
            }

            if view_response:
                response_dict[name] = view_response
        elif cache['json']:
            response_dict[name] = cache['json']

    return JsonResponse(response_dict)
