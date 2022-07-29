import pytest

from ....tables import users
from ....users.models import User
from ..mapper import ObjectMapper

mapper = ObjectMapper()

mapper.set_mapping(users, User)
root_query = mapper.query_table(users)


@pytest.mark.asyncio
async def test_results_can_be_filtered_with_ilike(admin):
    assert await root_query.filter(name__ilike="admin").count() == 1
    assert await root_query.filter(name__ilike="user").count() == 0


@pytest.mark.asyncio
async def test_results_can_be_filtered_with_contains(admin):
    assert await root_query.filter(name__contains="min").count() == 1
    assert await root_query.filter(name__contains="se").count() == 0


@pytest.mark.asyncio
async def test_results_can_be_filtered_with_icontains(admin):
    assert await root_query.filter(name__icontains="mIn").count() == 1
    assert await root_query.filter(name__icontains="min").count() == 1
    assert await root_query.filter(name__icontains="ser").count() == 0
    assert await root_query.filter(name__icontains="sEr").count() == 0


@pytest.mark.asyncio
async def test_results_can_be_filtered_with_startswith(admin):
    assert await root_query.filter(name__startswith="Ad").count() == 1
    assert await root_query.filter(name__startswith="ad").count() == 0


@pytest.mark.asyncio
async def test_results_can_be_filtered_with_istartswith(admin):
    assert await root_query.filter(name__istartswith="Ad").count() == 1
    assert await root_query.filter(name__istartswith="ad").count() == 1
    assert await root_query.filter(name__istartswith="us").count() == 0


@pytest.mark.asyncio
async def test_results_can_be_filtered_with_endswith(admin):
    assert await root_query.filter(name__endswith="in").count() == 1
    assert await root_query.filter(name__endswith="er").count() == 0


@pytest.mark.asyncio
async def test_results_can_be_filtered_with_iendswith(admin):
    assert await root_query.filter(name__iendswith="In").count() == 1
    assert await root_query.filter(name__iendswith="in").count() == 1
    assert await root_query.filter(name__iendswith="er").count() == 0
    assert await root_query.filter(name__iendswith="Er").count() == 0


@pytest.mark.asyncio
async def test_results_can_be_excluded_with_ilike(admin):
    assert await root_query.exclude(name__ilike="admin").count() == 0
    assert await root_query.exclude(name__ilike="user").count() == 1


@pytest.mark.asyncio
async def test_results_can_be_excluded_with_contains(admin):
    assert await root_query.exclude(name__contains="min").count() == 0
    assert await root_query.exclude(name__contains="se").count() == 1


@pytest.mark.asyncio
async def test_results_can_be_excluded_with_icontains(admin):
    assert await root_query.exclude(name__icontains="mIn").count() == 0
    assert await root_query.exclude(name__icontains="min").count() == 0
    assert await root_query.exclude(name__icontains="ser").count() == 1
    assert await root_query.exclude(name__icontains="sEr").count() == 1


@pytest.mark.asyncio
async def test_results_can_be_excluded_with_startswith(admin):
    assert await root_query.exclude(name__startswith="Ad").count() == 0
    assert await root_query.exclude(name__startswith="ad").count() == 1


@pytest.mark.asyncio
async def test_results_can_be_excluded_with_istartswith(admin):
    assert await root_query.exclude(name__istartswith="Ad").count() == 0
    assert await root_query.exclude(name__istartswith="ad").count() == 0
    assert await root_query.exclude(name__istartswith="us").count() == 1
    assert await root_query.exclude(name__istartswith="Us").count() == 1


@pytest.mark.asyncio
async def test_results_can_be_excluded_with_endswith(admin):
    assert await root_query.exclude(name__endswith="in").count() == 0
    assert await root_query.exclude(name__endswith="er").count() == 1


@pytest.mark.asyncio
async def test_results_can_be_excluded_with_iendswith(admin):
    assert await root_query.exclude(name__iendswith="In").count() == 0
    assert await root_query.exclude(name__iendswith="in").count() == 0
    assert await root_query.exclude(name__iendswith="er").count() == 1
    assert await root_query.exclude(name__iendswith="Er").count() == 1


@pytest.mark.asyncio
async def test_matching_escapes_value(admin):
    # pylint: disable=anomalous-backslash-in-string
    assert await root_query.filter(name__ilike="%min").count() == 0
    assert await root_query.filter(name__ilike="\%min").count() == 0

    await admin.update(name="A%min")
    assert await root_query.filter(name__contains="%min").count() == 1
    assert await root_query.filter(name__contains="\%min").count() == 0
