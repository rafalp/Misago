from typing import Awaitable

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo

from ...forumstats.loaders import load_forum_stats
from .forumstats import ForumStatsType


class ForumStatsQueries(ObjectType):
    __schema__ = gql(
        """
        type Query {
            forumStats: ForumStats!
        }
        """
    )
    __aliases__ = {"forumStats": "forum_stats"}
    __requires__ = [ForumStatsType]

    @staticmethod
    def resolve_forum_stats(_, info: GraphQLResolveInfo) -> Awaitable[dict]:
        return load_forum_stats(info.context)
