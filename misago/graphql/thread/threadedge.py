from ariadne_graphql_modules import ObjectType, gql

from ...threads.models import Thread
from .thread import ThreadType


class ThreadEdgeType(ObjectType):
    __schema__ = gql(
        """
        type ThreadEdge {
            node: Thread!
            cursor: ID!
        }
        """
    )
    __aliases__ = {
        "cursor": "last_post_id",
    }
    __requires__ = [ThreadType]

    @staticmethod
    def resolve_node(obj: Thread, *_):
        return obj
