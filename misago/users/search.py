from django.utils.translation import ugettext_lazy as _

from misago.search import SearchProvider


class SearchUsers(SearchProvider):
    name = _("Search users")
    url = 'users'
