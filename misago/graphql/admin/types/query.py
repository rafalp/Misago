from typing import Awaitable, List, Optional

from ariadne import QueryType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo

from ....categories.models import Category
from ....loaders import load_root_categories
from ....users.get import get_users_list
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
    _, info: GraphQLResolveInfo, *, filters: Optional[dict] = None
) -> Awaitable[List[Category]]:
    filters = filters or {}

    users = get_users_list(**filters)
    await users.count_pages()
    return users
