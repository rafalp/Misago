from django.core.exceptions import PermissionDenied


class AjaxError(Exception):
    """you've tried to do something over AJAX but misago blurped"""

    def __init__(self, message=None, code=406):
        self.message = message
        self.code = code


class Banned(PermissionDenied):
    def __init__(self, ban=None):
        if ban:
            self.ban = ban


class ExplicitFirstPage(Exception):
    """the url that was used to reach view contained explicit first page"""
    pass


class OutdatedSlug(Exception):
    """the url that was used to reach view contained outdated slug"""
    pass
