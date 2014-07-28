from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponsePermanentRedirect, JsonResponse

from misago.core import errorpages
from misago.core.exceptions import AjaxError, ExplicitFirstPage, OutdatedSlug


HANDLED_EXCEPTIONS = (AjaxError, ExplicitFirstPage, Http404,
                      OutdatedSlug, PermissionDenied)


def is_misago_exception(exception):
    return exception.__class__ in HANDLED_EXCEPTIONS


def handle_ajax_error(request, exception):
    json = {'is_error': 1, 'message': exception.message}
    return JsonResponse(json, status=exception.code)


def handle_explicit_first_page_exception(request, exception):
    matched_url = request.resolver_match.url_name
    if request.resolver_match.namespace:
        matched_url = '%s:%s' % (request.resolver_match.namespace, matched_url)

    url_kwargs = request.resolver_match.kwargs
    del url_kwargs['page']

    new_url = reverse(matched_url, kwargs=url_kwargs)
    return HttpResponsePermanentRedirect(new_url)


def handle_http404_exception(request, exception):
    return errorpages.page_not_found(request)


def handle_outdated_slug_exception(request, exception):
    matched_url = request.resolver_match.url_name
    if request.resolver_match.namespace:
        matched_url = '%s:%s' % (request.resolver_match.namespace, matched_url)

    model = exception.args[0]
    model_name = model.__class__.__name__.lower()
    url_kwargs = request.resolver_match.kwargs
    url_kwargs['%s_slug' % model_name] = model.slug

    new_url = reverse(matched_url, kwargs=url_kwargs)
    return HttpResponsePermanentRedirect(new_url)


def handle_permission_denied_exception(request, exception):
    try:
        error_message = exception.args[0]
    except IndexError:
        error_message = None

    return errorpages.permission_denied(request, error_message)


EXCEPTION_HANDLERS = (
    (AjaxError, handle_ajax_error),
    (Http404, handle_http404_exception),
    (ExplicitFirstPage, handle_explicit_first_page_exception),
    (OutdatedSlug, handle_outdated_slug_exception),
    (PermissionDenied, handle_permission_denied_exception),
)


def get_exception_handler(exception):
    for exception_type, handler in EXCEPTION_HANDLERS:
        if isinstance(exception, exception_type):
            return handler
    else:
        raise ValueError(
            "%s is not Misago exception" % exception.__class__.__name__)


def handle_misago_exception(request, exception):
    handler = get_exception_handler(exception)
    return handler(request, exception)
