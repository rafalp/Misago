from django.core.exceptions import PermissionDenied

from ..search import SearchProvider


class AllowedProvider(SearchProvider):
    name = "Allowed provider"
    url = 'allowed-provider'


class ForbiddenProvider(SearchProvider):
    name = "Forbidden provider"
    url = 'forbidden-provider'

    def allow_search(self):
        raise PermissionDenied("You can't search this, dave")
