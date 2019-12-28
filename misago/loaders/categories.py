from typing import Dict, Optional, List, Union

from ..categories import CategoryTypes
from ..categories.get import get_all_categories
from ..types import GraphQLContext, Category
from .loader import positive_int


CACHE_NAME = "__categories"


async def load_categories_from_db(context: GraphQLContext) -> Dict[int, Category]:
    if CACHE_NAME not in context:
        context[CACHE_NAME] = {c.id: c for c in await get_all_categories()}
    return context[CACHE_NAME]


async def load_category(
    context: GraphQLContext,
    category_id: Union[int, str],
    category_type: Optional[int] = CategoryTypes.THREADS,
) -> Optional[Category]:
    internal_id = positive_int(category_id)
    if internal_id:
        categories = await load_categories_from_db(context)
        category = categories.get(internal_id)
        if category and category.type == category_type:
            return category
    return None


async def load_categories(
    context: GraphQLContext, category_type: Optional[int] = CategoryTypes.THREADS
) -> List[Category]:
    categories = await load_categories_from_db(context)
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

    categories = await load_categories_from_db(context)
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
