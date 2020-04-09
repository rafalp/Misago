import pytest

from ..category import (
    resolve_children,
    resolve_banner,
    resolve_color,
    resolve_icon,
    resolve_parent,
)


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
    category, graphql_info
):
    value = resolve_color(category, graphql_info)
    assert value == "#FF7452"


def test_category_icon_resolver_returns_string_with_category_color(
    category, graphql_info
):
    value = resolve_icon(category, graphql_info)
    assert value == "fas fa-adjust"


def test_category_banner_resolver_returns_dict_with_category_banners(
    category, graphql_info
):
    value = resolve_banner(category, graphql_info)
    assert value == {
        "full": {
            "align": "center",
            "background": "#2c3e50",
            "height": 100,
            "url": "http://lorempixel.com/1280/200/",
        },
        "half": {
            "align": "center",
            "background": "#2c3e50",
            "height": 100,
            "url": "http://lorempixel.com/768/200/",
        },
    }


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
