import pytest

from ..searchresults import resolve_users


@pytest.mark.asyncio
async def test_search_users_resolver_searches_users(db, user, graphql_info):
    results = await resolve_users(user.name, graphql_info)
    assert results[0].id == user.id


@pytest.mark.asyncio
async def test_search_users_resolver_limits_search_results(db, user, graphql_info):
    results = await resolve_users(user.name, graphql_info, limit=0)
    assert results == []
