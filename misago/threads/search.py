from django.utils.translation import ugettext_lazy as _

from misago.search import SearchProvider


class SearchThreads(SearchProvider):
    name = _("Threads")
    url = 'threads'
