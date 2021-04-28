from typing import Iterable, Protocol

from ...hooks import FilterHook
from ..models import Category


class MoveCategoriesContentsAction(Protocol):
    async def __call__(self, categories: Iterable[Category], new_category: Category):
        ...


class MoveCategoriesContentsFilter(Protocol):
    async def __call__(
        self,
        action: MoveCategoriesContentsAction,
        categories: Iterable[Category],
        new_category: Category,
    ):
        ...


class MoveCategoriesContentsHook(
    FilterHook[MoveCategoriesContentsAction, MoveCategoriesContentsFilter]
):
    async def call_action(
        self,
        action: MoveCategoriesContentsAction,
        categories: Iterable[Category],
        new_category: Category,
    ):
        await self.filter(action, categories, new_category)


move_categories_contents_hook = MoveCategoriesContentsHook()
