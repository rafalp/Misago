from typing import Awaitable, Iterable, List, Optional

from .models import Category, CategoryType


def get_all_categories(
    category_type: int = CategoryType.THREADS,
) -> Awaitable[List[Category]]:
    return Category.query.filter(type=category_type).order_by("left").all()


def get_categories(
    *,
    category_type: int = CategoryType.THREADS,
    parent_id: Optional[int] = None,
) -> Awaitable[List[Category]]:
    query = Category.query.filter(type=category_type)
    if parent_id:
        query = query.filter(parent_id=parent_id)
    return query.order_by("left").all()


def get_categories_by_id(
    ids: Iterable[int],
    category_type: int = CategoryType.THREADS,
) -> Awaitable[List[Category]]:
    return Category.query.filter(id__in=ids, type=category_type).order_by("left").all()


async def get_category_by_id(
    category_id: int, category_type: int = CategoryType.THREADS
) -> Optional[Category]:
    try:
        return await Category.query.one(type=category_type, id=category_id)
    except Category.DoesNotExist:
        return None
