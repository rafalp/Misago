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
    left: Optional[int] = 1,
    right: Optional[int] = 2,
    depth: Optional[int] = 0,
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
        "extra": extra or {},
    }

    data["id"] = await queries.insert(categories, **data)

    return Category(**data)
