from typing import List, Optional

from sqlalchemy import and_

from ..database import database
from ..tables import categories
from ..types import Category
from .categorytypes import CategoryTypes


async def get_all_categories(
    category_type: int = CategoryTypes.THREADS,
) -> List[Category]:
    query = (
        categories.select()
        .where(categories.c.type == category_type)
        .order_by(categories.c.left)
    )
    data = await database.fetch_all(query)
    return [Category(**row) for row in data]


async def get_category_by_id(
    category_id: int, category_type: int = CategoryTypes.THREADS
) -> Optional[Category]:
    query = categories.select().where(
        and_(categories.c.id == category_id, categories.c.type == category_type)
    )
    row = await database.fetch_one(query)
    return Category(**row) if row else None
