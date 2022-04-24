from typing import Awaitable, Optional

from ariadne_graphql_modules import InputType, ObjectType, gql
from graphql import GraphQLResolveInfo

from ...database.paginator import Page, Paginator
from ...users.loaders import users_loader
from ...users.models import User
from ..adminqueries import AdminQueries
from ..args import clean_id_arg, clean_page_arg, handle_invalid_args
from ..pagination import PageInfoType
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


class AdminUsersFilters(InputType):
    __schema__ = gql(
        """
        input UsersFilters {
            name: String
            email: String
            isActive: Boolean
            isModerator: Boolean
            isAdmin: Boolean
        }
        """
    )
    __args__ = {
        "isActive": "is_active",
        "isModerator": "is_moderator",
        "isAdmin": "is_admin",
    }


class AdminUsersPageType(ObjectType):
    __schema__ = gql(
        """
        type UsersPage {
            totalCount: Int!
            totalPages: Int!
            results: [User!]!
            pageInfo: PageInfo!
        }
        """
    )
    __aliases__ = {
        "totalCount": "total_count",
        "totalPages": "total_pages",
        "pageInfo": "page_info",
    }
    __requires__ = [AdminUserType, PageInfoType]


class AdminUserQueries(AdminQueries):
    __schema__ = gql(
        """
        type Query {
            user(id: ID!): User
            users(filters: UsersFilters, page: Int): UsersPage
        }
        """
    )
    __requires__ = [AdminUserType, AdminUsersPageType, AdminUsersFilters]

    @staticmethod
    @handle_invalid_args
    def resolve_user(
        _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
    ) -> Awaitable[Optional[User]]:
        user_id = clean_id_arg(id)
        return users_loader.load(info.context, user_id)

    @staticmethod
    @handle_invalid_args
    async def resolve_users(*_, filters: Optional[dict] = None, page: int = 1) -> Page:
        page = clean_page_arg(page)

        query = User.query

        if filters:
            if filters.get("name", "").strip():
                query = query.filter(slug__imatch=filters["name"])
            if filters.get("email", "").strip():
                query = query.filter(email__imatch=filters["email"])
            if filters.get("is_active") is not None:
                query = query.filter(is_active=filters["is_active"])
            if filters.get("is_admin") is not None:
                query = query.filter(is_admin=filters["is_admin"])
            if filters.get("is_moderator") is not None:
                query = query.filter(is_moderator=filters["is_moderator"])

        query = query.order_by("-id")

        paginator = Paginator(query, 50, 15)
        await paginator.count_pages()

        return await paginator.get_page(page)
