from typing import Awaitable, List

from ariadne import ObjectType

from ...types import User
from ...users.search import search_users


search_results_type = ObjectType("SearchResults")


@search_results_type.field("users")
def resolve_users(search_query: str, _, *, limit: int = 10) -> Awaitable[List[User]]:
    return search_users(search_query, limit=limit)
