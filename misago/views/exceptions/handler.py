from misago.views import exceptions


def is_misago_exception(exception):
    return exception.__class__ in exceptions.MISAGO_EXCEPTIONS


def handle_http404_exception(request, exception):
    raise NotImplementedError()


def handle_outdated_url_exception(request, exception):
    raise NotImplementedError()


def handle_permission_denied_exception(request, exception):
    raise NotImplementedError()


EXCEPTION_HANDLERS = (
    (exceptions.Http404, handle_http404_exception),
    (exceptions.OutdatedUrl, handle_outdated_url_exception),
    (exceptions.PermissionDenied, handle_permission_denied_exception),
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
