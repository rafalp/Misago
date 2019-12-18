from typing import Optional, List

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ...loaders import load_category, load_category_children
from ...types import Category


category_type = ObjectType("Category")


@category_type.field("parent")
async def resolve_parent(
    category: Category, info: GraphQLResolveInfo
) -> Optional[Category]:
    if category.parent_id:
        return await load_category(info.context, category.parent_id)
    return None


@category_type.field("children")
async def resolve_children(
    category: Category, info: GraphQLResolveInfo
) -> List[Category]:
    return await load_category_children(info.context, category.id)


@category_type.field("color")
def resolve_color(category: Category, info: GraphQLResolveInfo) -> str:
    color_offset = category.left - 1
    if color_offset > COLOR_PALETTE_SIZE:
        color_offset -= (color_offset // COLOR_PALETTE_SIZE) * color_offset
    return COLOR_PALETTE[color_offset]


COLOR_PALETTE = (
    "#FF5630",
    "#36B37E",
    "#0052CC",
    "#FFAB00",
    "#00B8D9",
    "#6554C0",
)

COLOR_PALETTE_SIZE = len(COLOR_PALETTE) - 1
