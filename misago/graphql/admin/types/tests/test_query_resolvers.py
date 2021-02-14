import pytest

from ..query import resolve_categories


@pytest.mark.asyncio
async def test_categories_resolver_returns_list_of_categories(
    category, child_category, admin_graphql_info
):
    value = await resolve_categories(None, admin_graphql_info)
    assert category in value
    assert child_category in value


@pytest.mark.asyncio
async def test_categories_resolver_returns_none_if_user_is_not_admin(
    category, child_category, user_graphql_info
):
    value = await resolve_categories(None, user_graphql_info)
    assert value is None
