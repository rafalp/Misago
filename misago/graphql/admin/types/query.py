from typing import Awaitable, List, Optional

from ariadne import QueryType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo

from ....categories.models import Category
from ....conf.types import Settings
from ....database.paginator import Paginator
from ....loaders import load_category, load_root_categories, load_user
from ....users.models import User
from ..decorators import admin_resolver

query_type = QueryType()


@query_type.field("category")
@admin_resolver
def resolve_category(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[Category]]:
    return load_category(info.context, id)


@query_type.field("categories")
@admin_resolver
def resolve_categories(_, info: GraphQLResolveInfo) -> Awaitable[List[Category]]:
    return load_root_categories(info.context)


@query_type.field("settings")
@admin_resolver
def resolve_settings(_, info: GraphQLResolveInfo) -> Settings:
    return info.context["settings"]


@query_type.field("user")
@admin_resolver
def resolve_user(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[User]]:
    return load_user(info.context, id)


@query_type.field("users")
@admin_resolver
@convert_kwargs_to_snake_case
async def resolve_users(
    *_, filters: Optional[dict] = None, sort: Optional[str] = None
) -> Paginator:
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
    return paginator
