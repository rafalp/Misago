from typing import Awaitable, List, Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ....loaders import load_category, load_category_children
from ....types import Category

category_type = ObjectType("Category")

category_type.set_alias("isClosed", "is_closed")


@category_type.field("parent")
def resolve_parent(
    category: Category, info: GraphQLResolveInfo
) -> Optional[Awaitable[Optional[Category]]]:
    if category.parent_id:
        return load_category(info.context, category.parent_id)
    return None


@category_type.field("children")
def resolve_children(
    category: Category, info: GraphQLResolveInfo
) -> Awaitable[List[Category]]:
    return load_category_children(info.context, category.id)


# placeholder resolver for icon
@category_type.field("icon")
def resolve_icon(category: Category, info: GraphQLResolveInfo) -> str:
    icon_offset = category.left - 1
    if icon_offset > ICONS_PALETTE_SIZE:
        icon_offset -= (icon_offset // ICONS_PALETTE_SIZE) * icon_offset
    return ICONS_PALETTE[icon_offset]


@category_type.field("banner")
def resolve_banner(category: Category, info: GraphQLResolveInfo) -> dict:
    return {
        "full": {
            "align": "center",
            "background": "#2c3e50",
            "height": 100,
            "url": "http://lorempixel.com/1280/200/",
        },
        "half": {
            "align": "center",
            "background": "#2c3e50",
            "height": 100,
            "url": "http://lorempixel.com/768/200/",
        },
    }


@category_type.field("extra")
def resolve_extra(category: Category, info: GraphQLResolveInfo) -> dict:
    return {}


ICONS_PALETTE = (
    "fas fa-pencil-ruler",
    "fas fa-rocket",
    "fas fa-heart",
    "fas fa-hammer",
    "fas fa-award",
    "fas fa-cog",
    "fas fa-adjust",
    "far fa-bookmark",
    "far fa-calendar",
    "fas fa-clinic-medical",
    "fas fa-coffee",
    "fas fa-car-battery",
    "far fa-compass",
    "far fa-envelope",
    "fas fa-flask",
    "far fa-image",
    "fas fa-paint-brush",
    "far fa-paper-plane",
    "fas fa-plane",
)

ICONS_PALETTE_SIZE = len(ICONS_PALETTE) - 1
