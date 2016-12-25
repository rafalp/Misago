from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _, ugettext_lazy

from misago.search import SearchProvider


class SearchUsers(SearchProvider):
    name = ugettext_lazy("Users")
    url = 'users'

    def allow_search(self):
        if not self.request.user.acl['can_search_users']:
            raise PermissionDenied(
                _("You don't have permission to search users."))
