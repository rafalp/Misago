from typing import Iterable

from ..types import (
    Category,
    DeleteCategoriesContentsAction,
    DeleteCategoriesContentsFilter,
)
from .filter import FilterHook


class DeleteCategoriesContentsHook(
    FilterHook[DeleteCategoriesContentsAction, DeleteCategoriesContentsFilter]
):
    async def call_action(
        self,
        action: DeleteCategoriesContentsAction,
        categories: Iterable[Category],
    ):
        await self.filter(action, categories)
