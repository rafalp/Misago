from typing import List

from ..database import database
from ..tables import categories
from ..types import Category
from .categorytypes import CategoryTypes


async def get_all_categories() -> List[Category]:
    query = (
        categories.select()
        .where(categories.c.type == CategoryTypes.THREADS)
        .order_by(categories.c.left)
    )
    data = await database.fetch_all(query)
    return [Category(**row) for row in data]
