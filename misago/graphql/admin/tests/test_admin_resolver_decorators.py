import pytest

from ....errors import NotAdminError
from ..decorators import admin_mutation, admin_query


@admin_mutation
def admin_mutation_resolver(*args, **kwargs):
    pass


@pytest.mark.asyncio
async def test_no_error_is_raised_when_mutation_resolver_is_called_with_admin_auth(
    admin_graphql_info,
):
    await admin_mutation_resolver(None, admin_graphql_info)


@pytest.mark.asyncio
async def test_not_admin_error_is_raised_when_mutation_resolver_is_called_without_admin_auth(
    user_graphql_info,
):
    with pytest.raises(NotAdminError):
        await admin_mutation_resolver(None, user_graphql_info)


@pytest.mark.asyncio
async def test_not_admin_error_is_raised_when_mutation_resolver_is_called_without_any_auth(
    graphql_info,
):
    with pytest.raises(NotAdminError):
        await admin_mutation_resolver(None, graphql_info)


@admin_query
def admin_query_resolver(*args, **kwargs):
    return True


@pytest.mark.asyncio
async def test_query_resolver_returns_value_when_called_with_admin_auth(
    admin_graphql_info,
):
    value = await admin_query_resolver(None, admin_graphql_info)
    assert value is True


@pytest.mark.asyncio
async def test_query_resolver_returns_none_when_called_without_admin_auth(
    user_graphql_info,
):
    value = await admin_query_resolver(None, user_graphql_info)
    assert value is None


@pytest.mark.asyncio
async def test_query_resolver_returns_none_when_called_without_any_auth(
    graphql_info,
):
    value = await admin_query_resolver(None, graphql_info)
    assert value is None
