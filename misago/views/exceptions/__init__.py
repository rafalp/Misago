from django.core.exceptions import PermissionDenied as DjPermissionDenied
from django.http import Http404 as DjHttp404


__all__ = ["Http404", "OutdatedUrl", "PermissionDenied"]


class Http404(DjHttp404):
    """The requested page could not be found"""
    pass


class OutdatedUrl(Exception):
    """The url that was used to reach view contained outdated slug"""
    pass


class PermissionDenied(DjPermissionDenied):
    """The user did not have permission to do that"""
    pass


MISAGO_EXCEPTIONS = (
    Http404,
    OutdatedUrl,
    PermissionDenied,
)
