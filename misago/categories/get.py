from typing import Awaitable, List, Optional

from .models import Category
from .types import CategoryTypes


def get_all_categories(
    category_type: int = CategoryTypes.THREADS,
) -> Awaitable[List[Category]]:
    return Category.query.filter(type=category_type).order_by("left").all()


async def get_category_by_id(
    category_id: int, category_type: int = CategoryTypes.THREADS
) -> Optional[Category]:
    try:
        return await Category.query.one(type=category_type, id=category_id)
    except Category.DoesNotExist:
        return None
