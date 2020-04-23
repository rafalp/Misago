from typing import Dict, Optional, List, Union

from ..categories import CategoryTypes
from ..categories.get import get_all_categories
from ..types import GraphQLContext, Category
from .loader import positive_int


CACHE_NAME = "__categories"


async def load_categories_dict(context: GraphQLContext) -> Dict[int, Category]:
    if CACHE_NAME not in context:
        context[CACHE_NAME] = await get_all_categories()
    return context[CACHE_NAME]


async def load_category(
    context: GraphQLContext,
    category_id: Union[int, str],
    category_type: Optional[int] = CategoryTypes.THREADS,
) -> Optional[Category]:
    internal_id = positive_int(category_id)
    if internal_id:
        categories = await load_categories_dict(context)
        category = categories.get(internal_id)
        if category and category.type == category_type:
            return category
    return None


async def load_categories(
    context: GraphQLContext, category_type: Optional[int] = CategoryTypes.THREADS
) -> List[Category]:
    categories = await load_categories_dict(context)
    return [c for c in categories.values() if c.type == category_type]


async def load_root_categories(
    context: GraphQLContext, category_type: Optional[int] = CategoryTypes.THREADS
) -> List[Category]:
    categories = await load_categories(context, category_type)
    return [c for c in categories if not c.depth]


async def load_category_children(
    context: GraphQLContext, category_id: Union[int, str]
) -> List[Category]:
    category = await load_category(context, category_id)
    if not category:
        return []

    categories = await load_categories_dict(context)
    return [c for c in categories.values() if c.is_child(category)]


async def load_category_with_children(
    context: GraphQLContext,
    category_id: Union[int, str],
    category_type: Optional[int] = CategoryTypes.THREADS,
) -> List[Category]:
    category = await load_category(context, category_id, category_type)
    if not category:
        return []

    return [category] + await load_category_children(context, category.id)


def store_category(context: GraphQLContext, category: Category):
    if CACHE_NAME not in context:
        return

    new_categories = context[CACHE_NAME].copy()
    new_categories[category.id] = category
    context[CACHE_NAME] = new_categories
