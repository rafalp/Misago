from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo

from .search import SearchType


class SearchQueries(ObjectType):
    __schema__ = gql(
        """
        type Query {
            search(query: String): Search!
        }
        """
    )
    __requires__ = [SearchType]

    @staticmethod
    def resolve_search(_, info: GraphQLResolveInfo, *, query: str) -> str:
        return query.strip()
