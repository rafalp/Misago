from typing import Awaitable, List, Optional

from ariadne import QueryType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo

from ....categories.models import Category
from ....database.paginator import Paginator
from ....loaders import load_root_categories
from ....users.models import User
from ..decorators import admin_query

query_type = QueryType()


@query_type.field("categories")
@admin_query
def resolve_categories(_, info: GraphQLResolveInfo) -> Awaitable[List[Category]]:
    return load_root_categories(info.context)


@query_type.field("users")
@admin_query
@convert_kwargs_to_snake_case
async def resolve_users(
    *_, filters: Optional[dict] = None, sort: Optional[str] = None
) -> Awaitable[List[Category]]:
    query = User.query

    if filters:
        if filters.get("name", "").strip():
            query = query.filter(slug__imatch=filters["name"])
        if filters.get("email", "").strip():
            query = query.filter(email__imatch=filters["email"])
        if filters.get("is_active") is not None:
            query = query.filter(is_active=filters["is_active"])
        if filters.get("is_administrator") is not None:
            query = query.filter(is_administrator=filters["is_administrator"])
        if filters.get("is_moderator") is not None:
            query = query.filter(is_moderator=filters["is_moderator"])

    query = query.order_by("-id")

    paginator = Paginator(query, 50, 15)
    await paginator.count_pages()
    return paginator
