from asyncio import Future
from typing import Dict, Optional, List, Union

from ..categories.get import get_all_categories
from ..types import GraphQLContext, Category
from ..utils.strings import parse_db_id
from .loader import list_loader


CACHE_NAME = "__categories"
DICT_CACHE_NAME = f"{CACHE_NAME}_dict"


@list_loader(CACHE_NAME)
async def load_categories(context: GraphQLContext) -> List[Category]:
    return await get_all_categories()


@list_loader(DICT_CACHE_NAME)
async def load_categories_dict(context: GraphQLContext) -> Dict[int, Category]:
    return {c.id: c for c in await load_categories(context)}


async def load_category(
    context: GraphQLContext, category_id: Union[int, str]
) -> Optional[Category]:
    internal_id = parse_db_id(category_id)
    if internal_id:
        categories = await load_categories_dict(context)
        return categories.get(internal_id)
    return None


async def load_root_categories(context: GraphQLContext) -> List[Category]:
    categories = await load_categories(context)
    return [c for c in categories if not c.depth]


async def load_category_children(
    context: GraphQLContext, category_id: Union[int, str]
) -> List[Category]:
    category = await load_category(context, category_id)
    if not category:
        return []

    categories = await load_categories(context)
    return [c for c in categories if c.is_child(category)]


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

    context.pop(DICT_CACHE_NAME, None)

    new_categories = []
    for cached_category in context[CACHE_NAME].result():
        if cached_category.id == category.id:
            new_categories.append(category)
        else:
            new_categories.append(cached_category)

    future: Future[List[Category]] = Future()
    future.set_result(new_categories)
    context[CACHE_NAME] = future
