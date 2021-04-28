from dataclasses import replace
from typing import Any, Dict, Optional, Union

from ..database.queries import update
from ..tables import categories
from ..utils.strings import slugify
from .models import Category


async def update_category(
    category: Category,
    *,
    name: Optional[str] = None,
    color: Optional[str] = None,
    icon: Optional[str] = None,
    parent: Optional[Union[Category, bool]] = None,
    left: Optional[int] = None,
    right: Optional[int] = None,
    depth: Optional[int] = None,
    threads: Optional[int] = None,
    increment_threads: Optional[bool] = False,
    posts: Optional[int] = None,
    increment_posts: Optional[bool] = False,
    is_closed: Optional[bool] = None,
    extra: Optional[Dict[str, Any]] = None
) -> Category:
    changes: Dict[str, Any] = {}

    if name is not None and name != category.name:
        changes["name"] = name
        changes["slug"] = slugify(name)

    if color is not None and color != category.color:
        changes["color"] = color.upper()

    if icon is not None and icon != category.icon:
        changes["icon"] = icon or None

    if parent is True:
        raise ValueError("'parent' must be of type 'None', 'False' or 'Category'")

    if parent and isinstance(parent, Category):
        if parent.id == category.id:
            raise ValueError("'category' can't be its own parent")
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

    if threads is not None and increment_threads:
        raise ValueError(
            "'threads' and 'increment_threads' options are mutually exclusive"
        )
    if threads is not None and threads != category.threads:
        changes["threads"] = threads
    if increment_threads:
        changes["threads"] = categories.c.threads + 1

    if posts is not None and increment_posts:
        raise ValueError("'posts' and 'increment_posts' options are mutually exclusive")
    if posts is not None and posts != category.posts:
        changes["posts"] = posts
    if increment_posts:
        changes["posts"] = categories.c.posts + 1

    if is_closed is not None and is_closed != category.is_closed:
        changes["is_closed"] = is_closed

    if extra is not None and extra != category.extra:
        changes["extra"] = extra

    if not changes:
        return category

    await update(categories, category.id, **changes)

    # replace SQL expressions with actual ints for use in new dataclass
    if increment_threads:
        changes["threads"] = category.threads + 1
    if increment_posts:
        changes["posts"] = category.posts + 1

    updated_category = replace(category, **changes)
    return updated_category
