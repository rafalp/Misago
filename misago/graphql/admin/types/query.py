from typing import List, cast

from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ....categories.get import get_categories_mptt
from ....types import Category
from ..decorators import admin_query


query_type = QueryType()


@query_type.field("categories")
@admin_query
async def resolve_categories(_, info: GraphQLResolveInfo) -> List[Category]:
    nodes = (await get_categories_mptt()).nodes()
    return cast(List[Category], nodes)
