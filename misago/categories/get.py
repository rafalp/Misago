from typing import Dict, Optional

from sqlalchemy import and_

from ..database import database
from ..tables import categories
from ..types import Category, MPTT
from .categorytypes import CategoryTypes


async def get_all_categories(
    category_type: int = CategoryTypes.THREADS,
) -> Dict[int, Category]:
    query = (
        categories.select()
        .where(categories.c.type == category_type)
        .order_by(categories.c.left)
    )
    data = [Category(**row) for row in await database.fetch_all(query)]

    # Aggregate child categories stats to parent categories, mutating data
    categories_dict = {}
    for category in data:
        categories_dict[category.id] = category
        if category.parent_id:
            parent = categories_dict[category.parent_id]
            parent.threads += category.threads
            parent.posts += category.posts

    return categories_dict


async def get_category_by_id(
    category_id: int, category_type: int = CategoryTypes.THREADS
) -> Optional[Category]:
    query = categories.select().where(
        and_(categories.c.id == category_id, categories.c.type == category_type)
    )
    row = await database.fetch_one(query)
    return Category(**row) if row else None


async def get_categories_mptt(category_type: int = CategoryTypes.THREADS,) -> MPTT:
    mptt = MPTT()

    categories = await get_all_categories(category_type)
    categories_map = {}
    for category in categories.values():
        categories_map[category.id] = category
        if category.parent_id:
            mptt.insert_node(category, parent=categories_map[category.parent_id])
        else:
            mptt.insert_node(category)

    return mptt
