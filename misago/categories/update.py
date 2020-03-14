from dataclasses import replace
from typing import Any, Dict, Optional, Union

from ..database.queries import update
from ..tables import categories
from ..types import Category
from ..utils.strings import slugify


async def update_category(
    category: Category,
    *,
    name: str = None,
    parent: Optional[Union[Category, bool]] = None,
    left: Optional[int] = None,
    right: Optional[int] = None,
    depth: Optional[int] = None,
    is_closed: Optional[bool] = None,
    extra: Optional[Dict[str, Any]] = None
) -> Category:
    changes: Dict[str, Any] = {}

    if name is not None and name != category.name:
        changes["name"] = name
        changes["slug"] = slugify(name)

    if parent is True:
        raise ValueError("'parent' must be of type 'None', 'False' or 'Category'")

    if parent and isinstance(parent, Category):
        if parent.id == category.id:
            raise ValueError("'category' can't be its own parent")
        if parent.parent_id:
            raise ValueError("'parent' can't be a child category")
        if parent.id != category.parent_id:
            changes["parent_id"] = parent.id
    elif parent is False and category.parent_id:
        changes["parent_id"] = None

    if left is not None and left != category.left:
        changes["left"] = left
    if right is not None and right != category.right:
        changes["right"] = right
    if depth is not None and depth != category.depth:
        changes["depth"] = depth

    if is_closed is not None and is_closed != category.is_closed:
        changes["is_closed"] = is_closed

    if extra is not None and extra != category.extra:
        changes["extra"] = extra

    if not changes:
        return category

    await update(categories, category.id, **changes)

    updated_category = replace(category, **changes)
    return updated_category