from dataclasses import dataclass
from typing import Any

import pytest

from ...tables import categories, settings, users
from ..mapper import Mapper


@pytest.mark.asyncio
async def test_all_results_are_retrieved(db):
    mapper = Mapper(settings)
    results = await mapper.all()
    assert results
    assert results[0]["name"]
    assert results[0]["value"]


@pytest.mark.asyncio
async def test_one_result_is_retrieved(db):
    mapper = Mapper(settings)
    result = await mapper.filter(name="forum_name").one()
    assert result
    assert result["name"]
    assert result["value"]


@pytest.mark.asyncio
async def test_multiple_results_exception_is_raised_when_one_is_expected(db):
    mapper = Mapper(settings)
    with pytest.raises(mapper.MultipleObjectsReturned):
        await mapper.one()


@pytest.mark.asyncio
async def test_does_not_exist_exception_is_raised_when_one_is_expected(db):
    mapper = Mapper(users)
    with pytest.raises(mapper.DoesNotExist):
        await mapper.one()


@pytest.mark.asyncio
async def test_query_is_filtered(db):
    mapper = Mapper(settings)
    results = await mapper.filter(name="forum_name").all()
    assert results
    assert results[0]["name"] == "forum_name"
    assert results[0]["value"] == "Misago"


@pytest.mark.asyncio
async def test_query_excludes_some_results(admin, user):
    mapper = Mapper(users)
    results = await mapper.exclude(is_administrator=False).all()
    assert results
    assert results[0]["id"] == admin.id
    assert results[0]["slug"] == admin.slug
    assert results[0]["email"] == admin.email


@pytest.mark.asyncio
async def test_filter_and_exclude_can_be_combined(admin, user):
    mapper = Mapper(users)
    results = await mapper.filter(is_active=True).exclude(is_administrator=False).all()
    assert results
    assert results[0]["id"] == admin.id
    assert results[0]["slug"] == admin.slug
    assert results[0]["email"] == admin.email


@pytest.mark.asyncio
async def test_query_can_be_filtered_using_in(category, sibling_category):
    mapper = Mapper(categories)
    results = await mapper.filter(id__in=[category.id, sibling_category.id]).all()
    assert len(results) == 2
    assert results[0]["id"] == category.id
    assert results[0]["name"] == category.name
    assert results[1]["id"] == sibling_category.id
    assert results[1]["name"] == sibling_category.name


@pytest.mark.asyncio
async def test_query_can_be_filtered_using_sql_alchemy_expression(
    category, sibling_category
):
    mapper = Mapper(categories)
    results = await mapper.filter(mapper.columns.id == category.id).all()
    assert len(results) == 1
    assert results[0]["id"] == category.id
    assert results[0]["name"] == category.name


@pytest.mark.asyncio
async def test_query_result_is_limited_to_given_columns(db):
    mapper = Mapper(settings)
    results = await mapper.filter(name="forum_name").all("name")
    assert results == [{"name": "forum_name"}]


@pytest.mark.asyncio
async def test_query_result_is_flat_list_of_given_columns(db):
    mapper = Mapper(settings)
    results = await mapper.filter(name="forum_name").all("name", flat=True)
    assert results == ["forum_name"]


@pytest.mark.asyncio
async def test_query_result_is_ordered_by_single_column(category, child_category):
    mapper = Mapper(categories)
    results = await (
        mapper.filter(id__in=[category.id, child_category.id])
        .order_by("left")
        .all("id", flat=True)
    )
    assert results == [category.id, child_category.id]


@pytest.mark.asyncio
async def test_query_result_is_ordered_desc_by_single_column(category, child_category):
    mapper = Mapper(categories)
    results = await (
        mapper.filter(id__in=[category.id, child_category.id])
        .order_by("-left")
        .all("id", flat=True)
    )
    assert results == [child_category.id, category.id]


@pytest.mark.asyncio
async def test_query_result_is_ordered_by_multiple_columns(
    category, child_category, sibling_category
):
    mapper = Mapper(categories)
    results = await (
        mapper.filter(id__in=[category.id, child_category.id, sibling_category.id])
        .order_by("depth", "left")
        .all("id", flat=True)
    )
    assert results == [category.id, sibling_category.id, child_category.id]


@pytest.mark.asyncio
async def test_query_result_is_ordered_desc_by_multiple_columns(
    category, child_category, sibling_category
):
    mapper = Mapper(categories)
    results = await (
        mapper.filter(id__in=[category.id, child_category.id, sibling_category.id])
        .order_by("depth", "-left")
        .all("id", flat=True)
    )
    assert results == [sibling_category.id, category.id, child_category.id]


@pytest.mark.asyncio
async def test_count_results_table_size(admin, user):
    mapper = Mapper(users)
    rows_count = await mapper.count()
    assert rows_count == 2


@pytest.mark.asyncio
async def test_count_can_be_filtered(admin, user):
    mapper = Mapper(users)
    rows_count = await mapper.filter(is_administrator=True).count()
    assert rows_count == 1


@pytest.mark.asyncio
async def test_delete_all_empties_table(admin, user):
    mapper = Mapper(users)

    rows_count = await mapper.count()
    assert rows_count == 2

    await mapper.delete_all()

    rows_count = await mapper.count()
    assert rows_count == 0


@pytest.mark.asyncio
async def test_delete_can_be_filtered(admin, user):
    mapper = Mapper(users)

    rows_count = await mapper.count()
    assert rows_count == 2

    await mapper.filter(is_administrator=False).delete()

    rows_count = await mapper.count()
    assert rows_count == 1


@pytest.mark.asyncio
async def test_insert_creates_new_row(db):
    mapper = Mapper(settings)
    result = await mapper.insert(name="test_setting", value="wololo")
    assert result
    assert result["name"] == "test_setting"
    assert result["value"] == "wololo"


@pytest.mark.asyncio
async def test_update_updates_all_rows(admin):
    assert admin.is_administrator

    mapper = Mapper(users)
    await mapper.update(is_administrator=False)

    admin_from_db = await mapper.filter(id=admin.id).one()
    assert not admin_from_db["is_administrator"]


@pytest.mark.asyncio
async def test_insert_sets_id_on_newly_created_row(db):
    mapper = Mapper(categories)
    result = await mapper.insert(
        name="Test",
        slug="test",
        type=1,
        depth=0,
        left=0,
        right=0,
        is_closed=False,
        extra={},
    )

    assert result
    assert result["id"]
    assert result["name"] == "Test"
    assert result["slug"] == "test"

    result_from_db = await mapper.filter(id=result["id"]).one()
    assert result["id"] == result_from_db["id"]
    assert result["name"] == result_from_db["name"]


@dataclass
class Model:
    name: str
    value: Any


@pytest.mark.asyncio
async def test_query_result_is_mapped_to_type(db):
    mapper = Mapper(settings, Model)
    results = await mapper.all()
    assert results
    assert isinstance(results[0], Model)
    assert results[0].name
    assert results[0].value
