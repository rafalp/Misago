from typing import Optional, Union

from ..auth.errors import NotModeratorError
from ..graphql import GraphQLContext
from ..loaders import load_category
from .errors import (
    CategoryInvalidParentError,
    CategoryIsClosedError,
    CategoryNotFoundError,
)
from .models import Category, CategoryType


class CategoryExistsValidator:
    _context: GraphQLContext
    _category_type: int

    def __init__(
        self, context: GraphQLContext, category_type: int = CategoryType.THREADS
    ):
        self._context = context
        self._category_type = category_type

    async def __call__(self, category_id: Union[int, str], *_) -> Category:
        category = await load_category(self._context, category_id)
        if not category or category.type != self._category_type:
            raise CategoryNotFoundError(category_id=category_id)
        return category


class CategoryIsOpenValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, category: Category, *_) -> Category:
        if category.is_closed:
            user = self._context["user"]
            if not (user and user.is_moderator):
                raise CategoryIsClosedError(category_id=category.id)
        return category


class CategoryModeratorValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
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
