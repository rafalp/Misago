import math
from dataclasses import dataclass
from typing import Optional, cast

from .models import Query


class PageInvalidError(Exception):
    pass


@dataclass
class Page:
    total_count: int
    total_pages: int
    results: list
    page_info: "PageInfo"


@dataclass
class PageInfo:
    number: int
    has_next_page: bool
    has_previous_page: bool
    next_page: Optional[int]
    previous_page: Optional[int]
    start: int
    stop: int


class Paginator:
    _query: Query
    _initialized: bool
    total_count: int
    total_pages: int
    per_page: int
    orphans: int
    overlap_pages: bool

    def __init__(
        self,
        query: Query,
        per_page: int,
        orphans: int = 0,
        *,
        overlap_pages: bool = False,
    ):
        self._query = query
        self._initialized = False
        self.total_count = 0
        self.total_pages = 0

        self.per_page = per_page
        self.orphans = orphans
        self.overlap_pages = overlap_pages

    async def count_pages(self):
        self._initialized = True
        self.total_count = await self._query.count()

        if self.overlap_pages:
            self.total_pages = count_pages_with_overlaps(
                self.total_count, self.per_page, self.orphans
            )
        else:
            self.total_pages = count_pages(
                self.total_count, self.per_page, self.orphans
            )

    async def get_page(self, page_number: int) -> Page:
        if not self._initialized:
            await self.count_pages()

        if page_number < 1:
            raise PageInvalidError()

        if page_number > self.total_pages:
            return self.create_blank_page(page_number)

        start = (page_number - 1) * self.per_page
        stop = start + self.per_page
        if stop + self.orphans >= self.total_count:
            stop = self.total_count

        results = cast(list, await self._query.offset(start).limit(stop - start).all())

        return Page(
            total_count=self.total_count,
            total_pages=self.total_pages,
            results=results,
            page_info=PageInfo(
                number=page_number,
                has_next_page=page_number < self.total_pages,
                has_previous_page=page_number > 1,
                next_page=page_number + 1 if page_number < self.total_pages else None,
                previous_page=page_number - 1 if page_number > 2 else None,
                start=start or 1,
                stop=stop,
            ),
        )

    def create_blank_page(self, page_number: int) -> Page:
        return Page(
            total_count=self.total_count,
            total_pages=self.total_pages,
            results=[],
            page_info=PageInfo(
                number=page_number,
                has_next_page=False,
                has_previous_page=True,
                next_page=None,
                previous_page=self.total_pages or 1,
                start=0,
                stop=0,
            ),
        )

    async def get_page_number_for_offset(self, item_offset: int) -> int:
        if not self._initialized:
            await self.count_pages()

        if self.total_pages < 2 or item_offset < self.per_page:
            return 1

        if self.overlap_pages:
            page = count_pages(item_offset, self.per_page - 1)
        else:
            page = count_pages(item_offset, self.per_page)

        return min(self.total_pages, page)


def count_pages(count: int, per_page: int, orphans: int = 0) -> int:
    items = max(1, count - orphans)
    return math.ceil(items / per_page)


def count_pages_with_overlaps(count: int, per_page: int, orphans: int = 0) -> int:
    if count - orphans <= per_page:
        return 1
    return count_pages(count, per_page - 1, orphans)
