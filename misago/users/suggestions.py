from typing import List

from sqlalchemy import asc, or_

from ..database import database
from ..database.queries import istartswith
from ..tables import users
from ..types import User


USERS_SUGGESTIONS_LIMIT = 10


async def find_users_suggestions(search: str) -> List[User]:
    search_lowercased = search.lower()

    query = (
        users.select(None)
        .where(
            or_(
                users.c.slug.startswith(search_lowercased),
                istartswith(users.c.full_name, search),
            )
        )
        .order_by(asc(users.c.slug))
        .limit(USERS_SUGGESTIONS_LIMIT)
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
