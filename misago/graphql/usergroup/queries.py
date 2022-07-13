from typing import Awaitable, List, Optional

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo

from ...users.loaders import users_groups_loader
from ...users.models import UserGroup
from ..adminqueries import AdminQueries
from ..args import clean_id_arg, handle_invalid_args
from .usergroup import AdminUserGroupType, UserGroupType


class UserGroupQueries(ObjectType):
    __schema__ = gql(
        """
        type Query {
            userGroups: [UserGroup!]!
            userGroup(id: ID!): UserGroup
        }
        """
    )
    __aliases__ = {
        "userGroups": "user_groups",
        "userGroup": "user_group",
    }
    __requires__ = [UserGroupType]

    @staticmethod
    def resolve_user_groups(*_) -> Awaitable[List[UserGroup]]:
        return UserGroup.query.filter(is_hidden=False).order_by("ordering").all()

    @staticmethod
    @handle_invalid_args
    async def resolve_user_group(
        _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
    ) -> Optional[UserGroup]:
        user_group_id = clean_id_arg(id)
        user_group = await users_groups_loader.load(info.context, user_group_id)
        if user_group and not user_group.is_hidden:
            return user_group

        return None


class AdminUserGroupQueries(AdminQueries):
    __schema__ = gql(
        """
        type Query {
            userGroups: [UserGroup!]
            userGroup(id: ID!): UserGroup
        }
        """
    )
    __aliases__ = {
        "userGroups": "user_groups",
        "userGroup": "user_group",
    }
    __requires__ = [AdminUserGroupType]

    @staticmethod
    def resolve_user_groups(*_) -> Awaitable[List[UserGroup]]:
        return UserGroup.query.order_by("ordering").all()

    @staticmethod
    @handle_invalid_args
    async def resolve_user_group(
        _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
    ) -> Optional[UserGroup]:
        user_group_id = clean_id_arg(id)
        return await users_groups_loader.load(info.context, user_group_id)
