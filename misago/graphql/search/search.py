from typing import Awaitable, List

from ariadne_graphql_modules import DeferredType, ObjectType, gql

from ...users.models import User
from ...users.search import search_users


class SearchType(ObjectType):
    __schema__ = gql(
        """
        type Search {
            users(limit: Int): [User!]!
        }
        """
    )
    __requires__ = [DeferredType("User")]

    @staticmethod
    def resolve_users(
        search_query: str, _, *, limit: int = 10
    ) -> Awaitable[List[User]]:
        return search_users(search_query, limit=limit)
