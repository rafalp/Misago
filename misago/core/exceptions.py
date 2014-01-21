from django.core.exceptions import PermissionDenied as DjPermissionDenied
from django.http import Http404 as DjHttp404


class PermissionDenied(DjPermissionDenied):
    """The user did not have permission to do that"""
    pass


class Http404(DjHttp404):
    """The requested page could not be found"""
    pass


class OutdatedUrl(Exception):
    """The url that was used to reach view contained outdated slug"""