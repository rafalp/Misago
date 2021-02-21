from asyncio import Future
from typing import Dict, Optional, List, Union

from ..categories import CategoryTypes
from ..categories.get import get_all_categories
from ..types import GraphQLContext, Category
from ..utils.strings import parse_db_id
from .loader import list_loader


CACHE_NAME = "__categories"


@list_loader(CACHE_NAME)
async def load_categories_dict(context: GraphQLContext) -> Dict[int, Category]:
    return {c.id: c for c in await get_all_categories()}


async def load_category(
    context: GraphQLContext, category_id: Union[int, str]
) -> Optional[Category]:
    internal_id = parse_db_id(category_id)
    if internal_id:
        categories = await load_categories_dict(context)
        return categories.get(internal_id)
    return None


async def load_categories(context: GraphQLContext) -> List[Category]:
    categories = await load_categories_dict(context)
    return list(categories.values())


async def load_root_categories(context: GraphQLContext) -> List[Category]:
    categories = await load_categories(context)
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
    context: GraphQLContext, category_id: Union[int, str],
) -> List[Category]:
    category = await load_category(context, category_id)
    if not category:
        return []

    return [category] + await load_category_children(context, category.id)


def store_category(context: GraphQLContext, category: Category):
    if CACHE_NAME not in context or not context[CACHE_NAME].done():
        return

    new_categories = context[CACHE_NAME].result()
    new_categories[category.id] = category

    future = Future()
    future.set_result(new_categories)
    context[CACHE_NAME] = future
