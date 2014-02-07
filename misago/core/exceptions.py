class ExplicitFirstPage(Exception):
    """The url that was used to reach view contained explicit first page"""
    pass


class OutdatedSlug(Exception):
    """The url that was used to reach view contained outdated slug"""
    pass
