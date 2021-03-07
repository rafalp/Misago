from typing import Iterable, Protocol

from .category import Category


class DeleteCategoriesContentsAction(Protocol):
    async def __call__(self, categories: Iterable[Category]):
        ...


class DeleteCategoriesContentsFilter(Protocol):
    async def __call__(
        self, action: DeleteCategoriesContentsAction, categories: Iterable[Category],
    ):
        ...
