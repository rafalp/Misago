# pylint: disable=super-init-not-called
from django.core.exceptions import PermissionDenied
from social_core.exceptions import AuthException


class AjaxError(Exception):
    """You've tried to do something over AJAX but misago blurped"""

    def __init__(self, message=None, code=406):
        self.message = message
        self.code = code


class Banned(PermissionDenied):
    def __init__(self, ban=None):
        if ban:
            self.ban = ban


class SocialAuthFailed(AuthException):
    """Exception used to return error messages from Misago's social auth to user."""

    def __init__(self, backend, message):
        self.backend = backend
        self.message = message


class SocialAuthBanned(AuthException):
    """Exception used to return ban message from Misago's social auth to user."""

    def __init__(self, backend, ban):
        self.backend = backend
        self.ban = ban


class ExplicitFirstPage(Exception):
    """The url that was used to reach view contained explicit first page"""


class OutdatedSlug(Exception):
    """The url that was used to reach view contained outdated slug"""
