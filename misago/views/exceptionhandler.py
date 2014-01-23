from django.core.exceptions import PermissionDenied
from django.http import Http404
from misago.views import errorpages
from misago.views.exceptions import OutdatedSlug


HANDLED_EXCEPTIONS = (Http404, OutdatedSlug, PermissionDenied,)


def is_misago_exception(exception):
    return exception.__class__ in HANDLED_EXCEPTIONS


def _get_exception_message(exception):
    try:
        return exception.args[0]
    except IndexError:
        return None


def handle_http404_exception(request, exception):
    return errorpages.page_not_found(request,
                                     _get_exception_message(exception))


def handle_outdated_slug_exception(request, exception):
    raise NotImplementedError()


def handle_permission_denied_exception(request, exception):
    return errorpages.permission_denied(request,
                                        _get_exception_message(exception))


EXCEPTION_HANDLERS = (
    (Http404, handle_http404_exception),
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
