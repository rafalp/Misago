from rest_framework.views import exception_handler as rest_exception_handler

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponsePermanentRedirect, JsonResponse
from django.urls import reverse
from django.utils import six

from . import errorpages
from .exceptions import AjaxError, Banned, ExplicitFirstPage, OutdatedSlug


HANDLED_EXCEPTIONS = [
    AjaxError,
    Banned,
    ExplicitFirstPage,
    Http404,
    OutdatedSlug,
    PermissionDenied,
]


def is_misago_exception(exception):
    return exception.__class__ in HANDLED_EXCEPTIONS


def handle_ajax_error(request, exception):
    json = {
        'is_error': 1,
        'message': six.text_type(exception.message),
    }
    return JsonResponse(json, status=exception.code)


def handle_banned_exception(request, exception):
    return errorpages.banned(request, exception)


def handle_explicit_first_page_exception(request, exception):
    matched_url = request.resolver_match.url_name
    if request.resolver_match.namespace:
        matched_url = '%s:%s' % (request.resolver_match.namespace, matched_url)

    url_kwargs = request.resolver_match.kwargs
    del url_kwargs['page']

    new_url = reverse(matched_url, kwargs=url_kwargs)
    return HttpResponsePermanentRedirect(new_url)


def handle_http404_exception(request, exception):
    return errorpages.page_not_found(request, exception)


def handle_outdated_slug_exception(request, exception):
    view_name = request.resolver_match.view_name

    model = exception.args[0]
    url_kwargs = request.resolver_match.kwargs
    url_kwargs['slug'] = model.slug

    new_url = reverse(view_name, kwargs=url_kwargs)
    return HttpResponsePermanentRedirect(new_url)


def handle_permission_denied_exception(request, exception):
    return errorpages.permission_denied(request, exception)


EXCEPTION_HANDLERS = [
    (AjaxError, handle_ajax_error),
    (Banned, handle_banned_exception),
    (Http404, handle_http404_exception),
    (ExplicitFirstPage, handle_explicit_first_page_exception),
    (OutdatedSlug, handle_outdated_slug_exception),
    (PermissionDenied, handle_permission_denied_exception),
]


def get_exception_handler(exception):
    for exception_type, handler in EXCEPTION_HANDLERS:
        if isinstance(exception, exception_type):
            return handler
    else:
        raise ValueError("%s is not Misago exception" % exception.__class__.__name__)


def handle_misago_exception(request, exception):
    handler = get_exception_handler(exception)
    return handler(request, exception)


def handle_api_exception(exception, context):
    response = rest_exception_handler(exception, context)
    if response:
        if isinstance(exception, Banned):
            response.data['ban'] = exception.ban.get_serialized_message()
        elif isinstance(exception, PermissionDenied):
            try:
                response.data['detail'] = exception.args[0]
            except IndexError:
                pass
        return response
    else:
        return None
