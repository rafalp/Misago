from typing import List

import pytest

from ....tables import attachment_types
from ..registry import MapperRegistry

mapper_registry = MapperRegistry()
root_query = mapper_registry.query_table(attachment_types)


async def consume_generator(generator) -> List[str]:
    results: List[str] = []
    async for result in generator:
        if isinstance(result, dict):
            results.append(result["name"])
        else:
            results.append(result.name)
    return results


@pytest.mark.asyncio
async def test_empty_table_can_be_batched(db):
    await root_query.delete_all()

    results = await consume_generator(root_query.batch())
    assert results == []


@pytest.mark.asyncio
async def test_small_table_can_be_batched(db):
    await root_query.delete_all()

    for i in range(1, 6):
        await root_query.insert(
            name=f"#{i}",
            extensions=[],
            mimetypes=[],
            size_limit=None,
            is_active=True,
        )

    results = await consume_generator(root_query.batch())
    assert results == ["#5", "#4", "#3", "#2", "#1"]


@pytest.mark.asyncio
async def test_small_table_can_be_batched_in_ascending_order(db):
    await root_query.delete_all()

    for i in range(1, 6):
        await root_query.insert(
            name=f"#{i}",
            extensions=[],
            mimetypes=[],
            size_limit=None,
            is_active=True,
        )

    results = await consume_generator(root_query.batch(descending=False))
    assert results == ["#1", "#2", "#3", "#4", "#5"]


@pytest.mark.asyncio
async def test_large_table_can_be_batched(db):
    await root_query.delete_all()

    for i in range(1, 41):
        await root_query.insert(
            name=f"#{i}",
            extensions=[],
            mimetypes=[],
            size_limit=None,
            is_active=True,
        )

    results = await consume_generator(root_query.batch())
    assert results == [f"#{i}" for i in reversed(range(1, 41))]


@pytest.mark.asyncio
async def test_large_table_can_be_batched_in_ascending_order(db):
    await root_query.delete_all()

    for i in range(1, 41):
        await root_query.insert(
            name=f"#{i}",
            extensions=[],
            mimetypes=[],
            size_limit=None,
            is_active=True,
        )

    results = await consume_generator(root_query.batch(descending=False))
    assert results == [f"#{i}" for i in range(1, 41)]


@pytest.mark.asyncio
async def test_filtered_query_can_be_batched(db):
    await root_query.delete_all()

    for i in range(1, 41):
        await root_query.insert(
            name=f"#{i}",
            extensions=[],
            mimetypes=[],
            size_limit=None,
            is_active=bool(i % 2),
        )

    results = await consume_generator(
        root_query.filter(is_active=True).batch(step_size=10)
    )
    assert results == [f"#{i}" for i in reversed(range(1, 41)) if i % 2 != 0]


@pytest.mark.asyncio
async def test_large_table_can_be_batched_on_some_columns(db):
    await root_query.delete_all()

    for i in range(1, 41):
        await root_query.insert(
            name=f"#{i}",
            extensions=[],
            mimetypes=[],
            size_limit=None,
            is_active=True,
        )

    results = await consume_generator(root_query.batch("id", "name"))
    assert results == [f"#{i}" for i in reversed(range(1, 41))]


@pytest.mark.asyncio
async def test_large_table_can_be_batched_as_flat_list(db):
    await root_query.delete_all()

    for i in range(1, 41):
        await root_query.insert(
            name=f"#{i}",
            extensions=[],
            mimetypes=[],
            size_limit=None,
            is_active=True,
        )

    results = []
    async for result in root_query.batch_flat("name"):
        results.append(result)

    assert results == [f"#{i}" for i in reversed(range(1, 41))]
