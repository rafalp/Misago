from ariadne_graphql_modules import ObjectType, gql

from ..connection import Connection, ConnectionResult
from ..pagination import PageInfoType
from .thread import ThreadType

thread_connection = Connection("-last_post_id")


class ThreadEdgeType(ObjectType):
    __schema__ = gql(
        """
        type ThreadEdge {
            node: Thread!
            cursor: ID!
        }
        """
    )
    __requires__ = [ThreadType]


class ThreadConnectionType(ObjectType):
    __schema__ = gql(
        """
        type ThreadConnection {
            totalCount: Int!
            edges: [ThreadEdge!]!
            pageInfo: PageInfo!
        }
        """
    )
    __aliases__ = {"totalCount": "total_count", "pageInfo": "page_info"}
    __requires__ = [ThreadEdgeType, PageInfoType]

    @staticmethod
    def resolve_total_count(obj: ConnectionResult, *_):
        return obj.query.count()
