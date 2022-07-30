from typing import Awaitable, Optional

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo

from ...database.models import Query, RootQuery
from ...users.loaders import users_loader
from ...users.models import User
from ..adminqueries import AdminQueries
from ..args import clean_id_arg, handle_invalid_args
from ..connection import ConnectionResult
from .connection import UserConnectionType, user_connection
from .filters import AdminUserFilters
from .sortby import AdminUserSortByEnum
from .user import AdminUserType, UserType


class UserQueries(ObjectType):
    __schema__ = gql(
        """
        type Query {
            user(id: ID!): User
        }
        """
    )
    __requires__ = [UserType]

    @staticmethod
    @handle_invalid_args
    async def resolve_user(
        _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
    ) -> Optional[User]:
        user_id = clean_id_arg(id)
        user = await users_loader.load(info.context, user_id)
        if user and user.is_active:
            return user

        return None


class AdminUserQueries(AdminQueries):
    __schema__ = gql(
        """
        type Query {
            users(
                first: Int,
                last: Int,
                after: ID,
                before: ID,
                filter: UserFilters,
                sortBy: UserSortBy! = JOINED_LAST,
            ): UserConnection
            user(id: ID!): User
        }
        """
    )
    __fields_args__ = {"users": {"sortBy": "sort_by"}}
    __requires__ = [
        AdminUserType,
        UserConnectionType,
        AdminUserSortByEnum,
        AdminUserFilters,
    ]

    @staticmethod
    async def resolve_users(
        _, info: GraphQLResolveInfo, **data: dict
    ) -> ConnectionResult:
        query: Query | RootQuery = User.query
        filters = data.get("filter")

        if filters:
            if filters.get("name", "").strip():
                query = query.filter(slug__simplesearch=filters["name"].lower())
            if filters.get("email", "").strip():
                query = query.filter(email__isimplesearch=filters["email"])
            if filters.get("is_active") is not None:
                query = query.filter(is_active=filters["is_active"])
            if filters.get("is_admin") is not None:
                query = query.filter(is_admin=filters["is_admin"])
            if filters.get("is_moderator") is not None:
                query = query.filter(is_moderator=filters["is_moderator"])

        return await user_connection.resolve(info.context, query, data, limit=100)

    @staticmethod
    @handle_invalid_args
    def resolve_user(
        _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
    ) -> Awaitable[Optional[User]]:
        user_id = clean_id_arg(id)
        return users_loader.load(info.context, user_id)
