from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ....categories.models import Category

category_type = ObjectType("Category")


@category_type.field("threads")
def resolve_threads(category: Category, info: GraphQLResolveInfo) -> int:
    categories_index = info.context["categories"]
    return categories_index[category.id].threads


@category_type.field("posts")
def resolve_posts(category: Category, info: GraphQLResolveInfo) -> int:
    categories_index = info.context["categories"]
    return categories_index[category.id].posts


@category_type.field("isClosed")
def resolve_is_closed(category: Category, info: GraphQLResolveInfo) -> bool:
    categories_index = info.context["categories"]
    return categories_index[category.id].is_closed
