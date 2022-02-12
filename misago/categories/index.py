from dataclasses import dataclass
from typing import Dict, List, Optional

from sqlalchemy.sql import select

from ..database import database
from .models import Category, CategoryType


@dataclass
class IndexCategory:
    id: int
    parent_id: Optional[int]
    threads: int
    posts: int
    is_closed: bool


class CategoriesIndex(Dict[int, IndexCategory]):
    @property
    def all_ids(self) -> List[int]:
        return list(self.keys())

    def get_children_ids(self, parent_id: int, include_parent=False) -> List[int]:
        ids = []
        for category in self.values():
            if category.id == parent_id and include_parent:
                ids.append(category.id)
            if category.parent_id == parent_id:
                ids.append(category.id)
        return ids


async def get_categories_index() -> CategoriesIndex:
    table = Category.table

    query = (
        select(
            table.c.id,
            table.c.parent_id,
            table.c.threads,
            table.c.posts,
            table.c.is_closed,
        )
        .where(table.c.type == CategoryType.THREADS)
        .order_by(table.c.left)
    )

    data = [IndexCategory(**row) for row in await database.fetch_all(query)]
    index = CategoriesIndex({c.id: c for c in data})

    # Propagate closed status downwards
    for category in data:
        if category.parent_id and index[category.parent_id].is_closed:
            category.is_closed = True

    # Aggregate stats upwards
    for category in reversed(data):
        if category.parent_id:
            index[category.parent_id].threads += category.threads
            index[category.parent_id].posts += category.posts

    return index
