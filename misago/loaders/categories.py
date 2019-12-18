from typing import Dict, Optional, List, Union

from ..categories.get import get_all_categories
from ..types import GraphQLContext, Category
from .loader import positive_int


CACHE_NAME = "__categories"


async def load_all_categories(context: GraphQLContext) -> Dict[int, Category]:
    if CACHE_NAME not in context:
        context[CACHE_NAME] = {c.id: c for c in await get_all_categories()}
    return context[CACHE_NAME]


async def load_category(
    context: GraphQLContext, category_id: Union[int, str]
) -> Optional[Category]:
    internal_id = positive_int(category_id)
    if internal_id:
        categories = await load_all_categories(context)
        return categories.get(internal_id)
    return None


async def load_categories(context: GraphQLContext) -> List[Category]:
    categories = await load_all_categories(context)
    return [c for c in categories.values() if not c.depth]


async def load_category_children(
    context: GraphQLContext, category_id: Union[int, str]
) -> List[Category]:
    category = await load_category(context, category_id)
    if not category:
        return []

    categories = await load_all_categories(context)
    return [c for c in categories.values() if c.is_child(category)]
