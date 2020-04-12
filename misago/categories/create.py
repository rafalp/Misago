from typing import Any, Dict, Optional

from ..database import queries
from ..tables import categories
from ..types import Category
from ..utils.strings import slugify
from .categorytypes import CategoryTypes


async def create_category(
    name: str,
    *,
    parent: Optional[Category] = None,
    left: Optional[int] = 0,
    right: Optional[int] = 0,
    depth: Optional[int] = 0,
    threads: Optional[int] = 0,
    posts: Optional[int] = 0,
    is_closed: Optional[bool] = False,
    extra: Optional[Dict[str, Any]] = None
) -> Category:
    data: Dict[str, Any] = {
        "type": CategoryTypes.THREADS,
        "name": name,
        "slug": slugify(name),
        "parent_id": parent.id if parent else None,
        "left": left,
        "right": right,
        "depth": depth,
        "threads": threads,
        "posts": posts,
        "is_closed": is_closed or False,
        "extra": extra or {},
    }

    data["id"] = await queries.insert(categories, **data)

    return Category(**data)
