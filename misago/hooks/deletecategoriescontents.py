from typing import Iterable, Protocol

from ..types import Category
from .filter import FilterHook


class DeleteCategoriesContentsAction(Protocol):
    async def __call__(self, categories: Iterable[Category]):
        ...


class DeleteCategoriesContentsFilter(Protocol):
    async def __call__(
        self,
        action: DeleteCategoriesContentsAction,
        categories: Iterable[Category],
    ):
        ...


class DeleteCategoriesContentsHook(
    FilterHook[DeleteCategoriesContentsAction, DeleteCategoriesContentsFilter]
):
    async def call_action(
        self,
        action: DeleteCategoriesContentsAction,
        categories: Iterable[Category],
    ):
        await self.filter(action, categories)


delete_categories_contents_hook = DeleteCategoriesContentsHook()
