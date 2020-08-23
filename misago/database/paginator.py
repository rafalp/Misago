import math

from sqlalchemy.sql import Select

from ..database.queries import count


class PageDoesNotExist(ValueError):
    pass


class Paginator:
    _query: Select
    _counted: bool
    _count: int
    _pages: int
    per_page: int
    orphans: int
    overlap_pages: bool

    def __init__(
        self,
        query: Select,
        per_page: int,
        orphans: int = 0,
        overlap_pages: bool = False,
    ):
        self._query = query
        self._counted = False
        self._count = 0
        self._pages = 0

        self.per_page = per_page
        self.orphans = orphans
        self.overlap_pages = overlap_pages

    def get_count(self) -> int:
        assert self._counted, "pagination is incomplete, use 'count_pages' first"
        return self._count

    def get_pages(self) -> int:
        assert self._counted, "pagination is incomplete, use 'count_pages' first"
        return self._pages

    async def count_pages(self):
        self._counted = True
        self._count = await count(self._query)

        if self.overlap_pages:
            self._pages = count_pages_with_overlaps(
                self._count, self.per_page, self.orphans
            )
        else:
            self._pages = count_pages(self._count, self.per_page, self.orphans)

    async def get_page(self, page_number: int) -> "Page":
        if not self._counted:
            await self.count_pages()

        if page_number < 1 or page_number > self._pages:
            raise PageDoesNotExist()

        start = (page_number - 1) * self.per_page
        stop = start + self.per_page
        if stop + self.orphans >= self._count:
            stop = self._count

        page_query = self._query.offset(start).limit(stop - start)
        return Page(page_query, page_number, start, stop, self)

    async def get_offset_page(self, item_offset: int) -> int:
        if not self._counted:
            await self.count_pages()

        if self._pages < 2 or item_offset < self.per_page:
            return 1

        if self.overlap_pages:
            page = count_pages(item_offset, self.per_page - 1)
        else:
            page = count_pages(item_offset, self.per_page)

        return min(self._pages, page)


def count_pages(count: int, per_page: int, orphans: int = 0) -> int:
    items = max(1, count - orphans)
    return math.ceil(items / per_page)


def count_pages_with_overlaps(count: int, per_page: int, orphans: int = 0) -> int:
    if count - orphans <= per_page:
        return 1
    return count_pages(count, per_page - 1, orphans)


class Page:
    _paginator: Paginator
    _query: Select

    number: int
    start: int
    stop: int

    is_first: bool
    is_last: bool
    has_previous: bool
    has_next: bool

    def __init__(
        self, query: Select, number: int, start: int, stop: int, paginator: Paginator
    ):
        self._paginator = paginator
        self._query = query

        self.number = number
        self.start = start
        self.stop = stop

        self.is_first = number == 1
        self.is_last = number == paginator._pages
        self.has_previous = number > 1
        self.has_next = number < paginator._pages

    @property
    def paginator(self) -> Paginator:
        return self._paginator

    @property
    def query(self) -> Select:
        return self._query
