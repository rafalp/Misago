from typing import TYPE_CHECKING

from .models import SearchLog

if TYPE_CHECKING:
    from ..users.models import User


def log_search(
    user: "User | None", ip_address: str, search_query: str, is_public: bool = False
) -> SearchLog:
    return SearchLog.objects.create(
        user=user, ip_address=ip_address, search_query=search_query, is_public=is_public
    )
