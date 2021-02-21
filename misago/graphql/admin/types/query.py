from typing import List, cast

from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ....categories.get import get_all_categories
from ....types import Category
from ..decorators import admin_query


query_type = QueryType()


@query_type.field("categories")
@admin_query
def resolve_categories(_, info: GraphQLResolveInfo) -> List[Category]:
    return get_all_categories()
