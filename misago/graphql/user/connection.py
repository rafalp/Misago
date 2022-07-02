from ariadne_graphql_modules import ObjectType, DeferredType, gql

from ..connection import Connection, ConnectionResult


class UserConnection(Connection):
    pass


user_connection = UserConnection()


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
        }
        """
    )
    __aliases__ = {"totalCount": "total_count"}
    __requires__ = [UserEdgeType]

    @staticmethod
    def resolve_total_count(obj: ConnectionResult, *_):
        return obj.query.count()
