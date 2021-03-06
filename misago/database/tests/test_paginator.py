import pytest
from sqlalchemy import desc

from ...tables import threads
from ..database import database
from ..paginator import (
    PageDoesNotExist,
    Paginator,
    count_pages,
    count_pages_with_overlaps,
)


@pytest.mark.asyncio
async def test_paginator_returns_page(thread, category):
    query = threads.select(None).where(threads.c.category_id == category.id)
    paginator = Paginator(query, 10)
    page = await paginator.get_page(1)
    query = page.query.order_by(desc(threads.c.last_post_id))
    assert await database.fetch_all(query)


@pytest.mark.asyncio
async def test_paginator_raises_page_not_exists_error_for_zero_page(thread, category):
    query = threads.select(None).where(threads.c.category_id == category.id)
    paginator = Paginator(query, 10)
    with pytest.raises(PageDoesNotExist):
        await paginator.get_page(0)


@pytest.mark.asyncio
async def test_paginator_allows_orphans_to_be_set(thread, category):
    query = threads.select(None).where(threads.c.category_id == category.id)
    paginator = Paginator(query, 10, orphans=1)
    page = await paginator.get_page(1)
    query = page.query.order_by(desc(threads.c.last_post_id))
    assert await database.fetch_all(query)


@pytest.mark.asyncio
async def test_paginator_allows_page_overlapping_to_be_set(thread, category):
    query = threads.select(None).where(threads.c.category_id == category.id)
    paginator = Paginator(query, 10, overlap_pages=True)
    page = await paginator.get_page(1)
    query = page.query.order_by(desc(threads.c.last_post_id))
    assert await database.fetch_all(query)


@pytest.mark.asyncio
async def test_paginator_returns_page_for_given_offset(thread, category):
    query = threads.select(None).where(threads.c.category_id == category.id)
    paginator = Paginator(query, 10)
    page = await paginator.get_offset_page(0)
    assert page == 1


@pytest.mark.asyncio
async def test_paginator_raises_page_not_exists_error_for_page_outside_range(
    thread, category
):
    query = threads.select(None).where(threads.c.category_id == category.id)
    paginator = Paginator(query, 10)
    with pytest.raises(PageDoesNotExist):
        await paginator.get_page(10)


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
