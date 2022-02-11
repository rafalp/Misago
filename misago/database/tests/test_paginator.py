import pytest

from ..paginator import (
    PageInvalidError,
    Paginator,
    count_pages,
    count_pages_with_overlaps,
)


@pytest.mark.asyncio
async def test_paginator_returns_page(thread, category):
    query = category.threads_query.order_by("-last_post_id")
    paginator = Paginator(query, 10)

    page = await paginator.get_page(1)
    assert page.results == [thread]

    assert page.page_info.number == 1
    assert page.page_info.has_next is False
    assert page.page_info.has_previous is False
    assert page.page_info.next is None
    assert page.page_info.previous is None
    assert page.page_info.start == 1
    assert page.page_info.stop == 1


@pytest.mark.asyncio
async def test_paginator_raises_page_invalid_error_for_zero_page(thread, category):
    query = category.threads_query.order_by("-last_post_id")
    paginator = Paginator(query, 10)
    with pytest.raises(PageInvalidError):
        await paginator.get_page(0)


@pytest.mark.asyncio
async def test_paginator_allows_orphans_to_be_set(thread, category):
    query = category.threads_query.order_by("-last_post_id")
    paginator = Paginator(query, 10, orphans=1)
    page = await paginator.get_page(1)
    assert page.results == [thread]


@pytest.mark.asyncio
async def test_paginator_allows_page_overlapping_to_be_set(thread, category):
    query = category.threads_query.order_by("-last_post_id")
    paginator = Paginator(query, 10, overlap_pages=True)
    page = await paginator.get_page(1)
    assert page.results == [thread]


@pytest.mark.asyncio
async def test_paginator_returns_empty_page_for_page_outside_range(thread, category):
    query = category.threads_query.order_by("-last_post_id")
    paginator = Paginator(query, 10)

    page = await paginator.get_page(10)
    assert page.results == []

    assert page.page_info.number == 10
    assert page.page_info.has_next is False
    assert page.page_info.has_previous is True
    assert page.page_info.next is None
    assert page.page_info.previous == 1
    assert page.page_info.start == 0
    assert page.page_info.stop == 0


@pytest.mark.asyncio
async def test_paginator_returns_page_number_for_given_offset(thread, category):
    query = category.threads_query.order_by("-last_post_id")
    paginator = Paginator(query, 10)
    page = await paginator.get_page_number_for_offset(0)
    assert page == 1


def test_there_is_always_at_least_one_page_if_no_items_exist():
    assert count_pages(0, 5, 0) == 1
    assert count_pages_with_overlaps(0, 5, 0) == 1


def test_pages_count_if_valid_for_pagination_data():
    assert count_pages(1, 5, 0) == 1
    assert count_pages_with_overlaps(1, 5, 0) == 1

    assert count_pages(5, 5, 0) == 1
    assert count_pages_with_overlaps(5, 5, 0) == 1

    assert count_pages(6, 5, 0) == 2
    assert count_pages_with_overlaps(6, 5, 0) == 2

    assert count_pages(10, 5, 0) == 2
    assert count_pages_with_overlaps(10, 5, 0) == 3

    assert count_pages(20, 5, 0) == 4
    assert count_pages_with_overlaps(20, 5, 0) == 5

    assert count_pages(100, 5, 0) == 20
    assert count_pages_with_overlaps(100, 5, 0) == 25


def test_pages_count_if_valid_for_pagination_data_with_orphans():
    assert count_pages(11, 10, 5) == 1
    assert count_pages_with_overlaps(11, 10, 5) == 1
    assert count_pages(15, 10, 5) == 1
    assert count_pages_with_overlaps(15, 10, 5) == 1
    assert count_pages(25, 10, 5) == 2
    assert count_pages_with_overlaps(25, 10, 5) == 3
