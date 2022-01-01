import pytest


CATEGORY_CHILDREN_QUERY = """
    query GetCategory($category: ID!) {
        category(id: $category) {
            id
            children {
                id
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_category_children_resolves_to_list_with_category_children(
    query_public_api, category, child_category
):
    result = await query_public_api(
        CATEGORY_CHILDREN_QUERY, {"category": str(category.id)}
    )
    assert result["data"] == {
        "category": {
            "id": str(category.id),
            "children": [{"id": str(child_category.id)}],
        }
    }


@pytest.mark.asyncio
async def test_category_children_resolves_to_empty_list_for_leaf_category(
    query_public_api, sibling_category
):
    result = await query_public_api(
        CATEGORY_CHILDREN_QUERY, {"category": str(sibling_category.id)}
    )
    assert result["data"] == {
        "category": {
            "id": str(sibling_category.id),
            "children": [],
        }
    }


@pytest.mark.asyncio
async def test_category_extra_resolves_to_empty_list_for_leaf_category(
    query_public_api, category
):
    query = """
        query GetCategory($category: ID!) {
            category(id: $category) {
                id
                extra
            }
        }
    """

    result = await query_public_api(query, {"category": str(category.id)})
    assert result["data"]["category"] == {
        "id": str(category.id),
        "extra": {},
    }


@pytest.mark.asyncio
async def test_category_banner_resolves_to_category_banners(query_public_api, category):
    query = """
        query GetCategory($category: ID!) {
            category(id: $category) {
                id
                banner {
                    full {
                        align
                        background
                        height
                        url
                    }
                    half {
                        align
                        background
                        height
                        url
                    }
                }
            }
        }
    """

    result = await query_public_api(query, {"category": str(category.id)})
    assert result["data"]["category"] == {
        "id": str(category.id),
        "banner": {
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
        },
    }


CATEGORY_PARENT_QUERY = """
    query GetCategory($category: ID!) {
        category(id: $category) {
            id
            parent {
                id
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_category_parent_resolves_to_category_parent(
    query_public_api, category, child_category
):
    result = await query_public_api(
        CATEGORY_PARENT_QUERY, {"category": str(child_category.id)}
    )
    assert result["data"]["category"] == {
        "id": str(child_category.id),
        "parent": {
            "id": str(category.id),
        },
    }


@pytest.mark.asyncio
async def test_category_parent_resolves_to_none_for_top_level_category(
    query_public_api, category
):
    result = await query_public_api(
        CATEGORY_PARENT_QUERY, {"category": str(category.id)}
    )
    assert result["data"]["category"] == {
        "id": str(category.id),
        "parent": None,
    }
