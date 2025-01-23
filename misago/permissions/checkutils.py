from contextlib import contextmanager

from django.core.exceptions import PermissionDenied
from django.http import Http404


class PermissionCheckResult:
    error: Http404 | PermissionDenied | None

    def __init__(self):
        self.error = None

    def __bool__(self):
        return not self.error

    @property
    def not_found(self) -> bool:
        return isinstance(self.error, Http404)

    @property
    def permission_denied(self) -> bool:
        return isinstance(self.error, PermissionDenied)


@contextmanager
def check_permissions():
    result = PermissionCheckResult()
    try:
        yield result
    except (Http404, PermissionDenied) as error:
        result.error = error
