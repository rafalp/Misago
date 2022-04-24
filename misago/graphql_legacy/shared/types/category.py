from typing import Awaitable, List, Optional, Union

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ....categories.loaders import categories_children_loader, categories_loader
from ....categories.models import Category

category_type = ObjectType("Category")

category_type.set_alias("isClosed", "is_closed")


@category_type.field("parent")
def resolve_parent(
    category: Category, info: GraphQLResolveInfo
) -> Optional[Awaitable[Optional[Category]]]:
    if category.parent_id:
        return categories_loader.load(info.context, category.parent_id)
    return None


@category_type.field("children")
def resolve_children(
    category: Category, info: GraphQLResolveInfo
) -> Union[Awaitable[List[Category]], List[Category]]:
    if category.has_children():
        return categories_children_loader.load(info.context, category.id)

    return []


@category_type.field("banner")
def resolve_banner(category: Category, info: GraphQLResolveInfo) -> dict:
    return {
        "full": {
            "align": "center",
            "background": "#2c3e50",
            "height": 100,
            "url": "http://placekitten.com/1280/200/",
        },
        "half": {
            "align": "center",
            "background": "#2c3e50",
            "height": 100,
            "url": "http://placekitten.com/768/200/",
        },
    }


@category_type.field("extra")
def resolve_extra(category: Category, info: GraphQLResolveInfo) -> dict:
    return {}