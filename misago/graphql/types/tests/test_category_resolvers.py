import pytest

from ..category import resolve_children, resolve_color, resolve_parent


@pytest.mark.asyncio
async def test_category_children_resolver_returns_list_with_category_children(
    category, child_category, graphql_info
):
    value = await resolve_children(category, graphql_info)
    assert value == [child_category]


@pytest.mark.asyncio
async def test_category_children_resolver_returns_empty_list_for_leaf_category(
    sibling_category, graphql_info
):
    value = await resolve_children(sibling_category, graphql_info)
    assert value == []


def test_category_color_resolver_returns_string_with_category_color(
    category, child_category, graphql_info
):
    value = resolve_color(category, graphql_info)
    assert value == "#FF5630"


@pytest.mark.asyncio
async def test_category_parent_resolver_returns_category_parent(
    category, child_category, graphql_info
):
    value = await resolve_parent(child_category, graphql_info)
    assert value == category


@pytest.mark.asyncio
async def test_category_parent_resolver_returns_none_for_top_level_category(
    category, graphql_info
):
    value = await resolve_parent(category, graphql_info)
    assert value is None
