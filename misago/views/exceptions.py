"""
Extra exceptions that can be raised by Misago Views
"""

class OutdatedSlug(Exception):
    """The url that was used to reach view contained outdated slug"""
    pass
