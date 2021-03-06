from typing import List

from sqlalchemy import asc, or_

from ..database import database
from ..database.queries import istartswith
from ..tables import users
from ..types import User

RESULTS_MAX_LIMIT = 50


async def search_users(search: str, *, limit: int = 10) -> List[User]:
    search_lowercased = search.lower()
    safe_limit = limit if limit <= RESULTS_MAX_LIMIT else RESULTS_MAX_LIMIT

    if safe_limit < 1:
        return []

    query = (
        users.select(None)
        .where(
            or_(
                users.c.slug.startswith(search_lowercased),
                istartswith(users.c.full_name, search),
            )
        )
        .order_by(asc(users.c.slug))
        .limit(safe_limit)
    )

    rows = await database.fetch_all(query)
    results = [User(**row) for row in rows]

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
