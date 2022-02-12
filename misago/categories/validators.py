from typing import Optional

from ..auth.errors import NotModeratorError
from ..context import Context
from .errors import (
    CategoryInvalidParentError,
    CategoryIsClosedError,
    CategoryNotFoundError,
)
from .index import IndexCategory
from .loaders import categories_loader
from .models import Category


class CategoryExistsValidator:
    _context: Context

    def __init__(self, context: Context):
        self._context = context

    async def __call__(self, category_id: int, *_) -> Category:
        category = await categories_loader.load(self._context, category_id)
        if not category:
            raise CategoryNotFoundError(category_id=category_id)
        return category


class CategoryIsOpenValidator:
    _context: Context

    def __init__(self, context: Context):
        self._context = context

    async def __call__(self, category: Category, *_) -> Category:
        index_category: IndexCategory = self._context["categories"].get(category.id)
        if index_category.is_closed:
            user = self._context["user"]
            if not (user and user.is_moderator):
                raise CategoryIsClosedError(category_id=category.id)
        return category


class CategoryModeratorValidator:
    _context: Context

    def __init__(self, context: Context):
        self._context = context

    async def __call__(self, category: Category, *_) -> Category:
        user = self._context["user"]

        if not user or not user.is_moderator:
            raise NotModeratorError()
        return category


def validate_category_parent(
    category: Category, parent: Optional[Category]
) -> Optional[Category]:
    if parent:
        error = CategoryInvalidParentError(category_id=parent.id)
        if category.id == parent.id:
            raise error
        if parent.parent_id:
            raise error
        if category.is_parent(parent):
            raise error
        if category.has_children():
            raise error

    return parent
