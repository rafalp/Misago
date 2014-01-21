from misago.core import exceptions


MISAGO_EXCEPTIONS = (
    exceptions.PermissionDenied,
    exceptions.Http404,
    exceptions.OutdatedUrl,
)


def is_misago_exception(exception):
    return exception.__class__ in MISAGO_EXCEPTIONS