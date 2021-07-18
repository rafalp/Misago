from typing import List

from sqlalchemy import or_

from ..database.queries import istartswith
from .models import User

RESULTS_MAX_LIMIT = 50


async def search_users(search: str, *, limit: int = 10) -> List[User]:
    search_lowercased = search.lower()
    safe_limit = limit if limit <= RESULTS_MAX_LIMIT else RESULTS_MAX_LIMIT

    if safe_limit < 1:
        return []

    results = (
        await User.query.filter(
            or_(
                User.table.c.slug.startswith(search_lowercased),
                istartswith(User.table.c.full_name, search),
            )
        )
        .order_by("slug")
        .limit(safe_limit)
        .all()
    )

    # Bring exact matches for full name or slug to front of suggestions
    ordered_results = []
    for result in results:
        if result.slug == search or (
            result.full_name and result.full_name.lower() == search_lowercased
        ):
            ordered_results.append(result)

    for result in results:
        if result not in ordered_results:
            ordered_results.append(result)

    return ordered_results
