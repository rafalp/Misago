import pytest

from ..categories import create_fake_category


@pytest.mark.asyncio
async def test_fake_category_is_created(db, faker):
    assert await create_fake_category(faker)


@pytest.mark.asyncio
async def test_multiple_fake_categories_are_created(db, faker):
    for _ in range(5):
        assert await create_fake_category(faker)


@pytest.mark.asyncio
async def test_fake_child_category_is_created(faker, category):
    assert await create_fake_category(faker, parent=category)


@pytest.mark.asyncio
async def test_multiple_fake_child_categories_are_created(faker, category):
    for _ in range(5):
        assert await create_fake_category(faker, parent=category)
