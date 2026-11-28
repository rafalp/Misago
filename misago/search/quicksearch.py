from dataclasses import dataclass

from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import pgettext

from ..permissions.checkutils import check_permissions
from ..permissions.privatethreads import check_private_threads_permission
from ..permissions.search import check_search_permission, check_search_users_permission
from .hooks import get_quick_search_data_hook


@dataclass(frozen=True)
class QuickSearchScope:
    id: str
    name: str
    url: str


def get_quick_search_data(request: HttpRequest) -> dict | None:
    return get_quick_search_data_hook(_get_quick_search_data_action, request)


def _get_quick_search_data_action(request: HttpRequest) -> dict | None:
    return {
        "id": "quick-search",
        "template_name": "misago/quick_search/modal.html",
        "scopes": get_quick_search_scopes(request),
    }


def get_quick_search_scopes(request: HttpRequest) -> list[QuickSearchScope]:
    with check_permissions() as can_search:
        check_search_permission(request.user_permissions)

    if not can_search:
        return []

    scopes = [
        QuickSearchScope(
            id="threads",
            name=pgettext("quick search scope", "Threads"),
            url=reverse("misago:threads-quick-search"),
        ),
    ]

    with check_permissions():
        check_private_threads_permission(request.user_permissions)

        scopes.append(
            QuickSearchScope(
                id="private-threads",
                name=pgettext("quick search scope", "Private threads"),
                url=reverse("misago:private-threads-quick-search"),
            )
        )

    with check_permissions():
        check_search_users_permission(request.user_permissions)

        scopes.append(
            QuickSearchScope(
                id="users",
                name=pgettext("quick search scope", "Users"),
                url=reverse("misago:users-quick-search"),
            )
        )

    return scopes
