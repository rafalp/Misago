class AjaxError(Exception):
    """You've tried to do something over AJAX but misago blurped"""
    def __init__(self, message=None, code=406):
        self.message = message
        self.code = code


class ExplicitFirstPage(Exception):
    """The url that was used to reach view contained explicit first page"""
    pass


class OutdatedSlug(Exception):
    """The url that was used to reach view contained outdated slug"""
    pass
