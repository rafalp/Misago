from typing import List, Optional

from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ...auth import get_authenticated_user
from ...loaders import load_categories, load_category
from ...types import Category, Settings, User


query_type = QueryType()


@query_type.field("auth")
async def resolve_auth(_, info: GraphQLResolveInfo) -> Optional[User]:
    return await get_authenticated_user(info.context)


@query_type.field("categories")
async def resolve_categories(_, info: GraphQLResolveInfo) -> List:
    return await load_categories(info.context)


@query_type.field("category")
async def resolve_category(
    _, info: GraphQLResolveInfo, *, id: int  # pylint: disable=redefined-builtin
) -> Optional[Category]:
    return await load_category(info.context, id)


@query_type.field("settings")
def resolve_settings(_, info: GraphQLResolveInfo) -> Settings:
    return info.context["settings"]
