import pytest

from ..errors import AuthenticationGraphQLError, ForbiddenGraphQLError
from ..decorators import admin_query, admin_resolver


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


@admin_resolver
def resolve_admin_value(*args, **kwargs):
    return True


@pytest.mark.asyncio
async def test_admin_resolver_raises_authorization_error_called_without_any_auth(
    graphql_info,
):
    with pytest.raises(AuthenticationGraphQLError):
        await resolve_admin_value(None, graphql_info)


@pytest.mark.asyncio
async def test_admin_resolver_raises_forbidden_error_called_without_admin_auth(
    user_graphql_info,
):
    with pytest.raises(ForbiddenGraphQLError):
        await resolve_admin_value(None, user_graphql_info)


@pytest.mark.asyncio
async def test_admin_resolver_returns_value_when_called_with_admin_auth(
    admin_graphql_info,
):
    assert await resolve_admin_value(None, admin_graphql_info)
