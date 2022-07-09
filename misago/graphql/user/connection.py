from ariadne_graphql_modules import ObjectType, DeferredType, gql

from ..connection import Connection, ConnectionResult
from ..pagination import PageInfoType

user_connection = Connection()


class UserEdgeType(ObjectType):
    __schema__ = gql(
        """
        type UserEdge {
            node: User!
            cursor: ID!
        }
        """
    )
    __requires__ = [DeferredType("User")]


class UserConnectionType(ObjectType):
    __schema__ = gql(
        """
        type UserConnection {
            totalCount: Int!
            edges: [UserEdge!]!
            pageInfo: PageInfo!
        }
        """
    )
    __aliases__ = {"totalCount": "total_count", "pageInfo": "page_info"}
    __requires__ = [UserEdgeType, PageInfoType]

    @staticmethod
    def resolve_total_count(obj: ConnectionResult, *_):
        return obj.query.count()
