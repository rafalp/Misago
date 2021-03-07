from typing import Iterable, Protocol

from .category import Category


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
