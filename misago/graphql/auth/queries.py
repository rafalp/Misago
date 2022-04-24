from typing import Optional

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo

from ...users.models import User
from ..users import UserType


class AuthQueries(ObjectType):
    __schema__ = gql(
        """
        type Query {
            auth: User
        }
        """
    )
    __requires__ = [UserType]

    @staticmethod
    def resolve_auth(_, info: GraphQLResolveInfo) -> Optional[User]:
        return info.context["user"]
