from typing import Awaitable, List, Optional

from ariadne import QueryType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo

from ....categories.get import get_all_categories
from ....categories.loaders import categories_loader
from ....categories.models import Category
from ....conf.types import Settings
from ....database.paginator import Page, Paginator
from ....users.loaders import users_loader
from ....users.models import User
from ...cleanargs import clean_id_arg, clean_page_arg, invalid_args_handler
from ..decorators import admin_resolver

query_type = QueryType()


@query_type.field("category")
@admin_resolver
@invalid_args_handler
def resolve_category(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[Category]]:
    category_id = clean_id_arg(id)
    return categories_loader.load(info.context, category_id)


@query_type.field("categories")
@admin_resolver
def resolve_categories(_, info: GraphQLResolveInfo) -> Awaitable[List[Category]]:
    return get_all_categories()


@query_type.field("settings")
@admin_resolver
def resolve_settings(_, info: GraphQLResolveInfo) -> Settings:
    return info.context["settings"]


@query_type.field("user")
@admin_resolver
@invalid_args_handler
def resolve_user(
    _, info: GraphQLResolveInfo, *, id: str  # pylint: disable=redefined-builtin
) -> Awaitable[Optional[User]]:
    user_id = clean_id_arg(id)
    return users_loader.load(info.context, user_id)


@query_type.field("users")
@admin_resolver
@convert_kwargs_to_snake_case
@invalid_args_handler
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
