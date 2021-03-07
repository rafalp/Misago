from typing import Iterable

from ..types import (
    Category,
    MoveCategoriesContentsAction,
    MoveCategoriesContentsFilter,
)
from .filter import FilterHook


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
