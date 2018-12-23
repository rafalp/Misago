from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from ..search import SearchProvider
from .serializers import UserCardSerializer

HEAD_RESULTS = 8
TAIL_RESULTS = 8

User = get_user_model()


class SearchUsers(SearchProvider):
    name = gettext_lazy("Users")
    icon = "people"
    url = "users"

    def allow_search(self):
        if not self.request.user_acl["can_search_users"]:
            raise PermissionDenied(_("You don't have permission to search users."))

    def search(self, query, page=1):
        if query:
            results = search_users(
                search_disabled=self.request.user.is_staff, username=query
            )
        else:
            results = []

        return {
            "results": UserCardSerializer(results, many=True).data,
            "count": len(results),
        }


def search_users(**filters):
    queryset = User.objects.order_by("slug").select_related(
        "rank", "ban_cache", "online_tracker"
    )

    if not filters.get("search_disabled", False):
        queryset = queryset.filter(is_active=True)

    username = filters.get("username").lower()

    results = []

    # lets grab head and tail results:
    results += list(queryset.filter(slug__startswith=username)[:HEAD_RESULTS])
    results += list(
        queryset.filter(slug__contains=username).exclude(
            pk__in=[r.pk for r in results]
        )[:TAIL_RESULTS]
    )

    return results
