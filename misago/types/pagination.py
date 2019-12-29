from dataclasses import dataclass, field
from typing import Generic, List, TypeVar

from ..database.paginator import Page


Item = TypeVar("Item")


@dataclass
class PaginationPage(Generic[Item]):
    """
    Pagination representation for GraphQL and UI usages
    """

    number: int
    start: int
    stop: int
    is_first: bool
    is_last: bool
    has_previous: bool
    has_next: bool
    pagination: "Pagination"
    items: List[Item] = field(default_factory=list)

    @classmethod
    def from_paginator_page(cls, page: Page, items: List[Item]):
        return cls(
            items=items,
            number=page.number,
            start=page.is_first + 1,
            stop=page.is_last,
            is_first=page.is_first,
            is_last=page.is_last,
            has_previous=page.has_previous,
            has_next=page.has_next,
            pagination=Pagination(
                count=page.paginator.get_count(),
                pages=page.paginator.get_pages(),
                pageSize=page.paginator.per_page,
            ),
        )


@dataclass
class Pagination:
    count: int
    pages: int
    pageSize: int
