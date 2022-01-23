import pytest

CATEGORIES_QUERY = """
    query GetCategories {
        categories {
            id
            threads
            posts
        }
    }
"""


@pytest.mark.asyncio
async def test_categories_query_resolves_to_only_top_level_categories(
    query_public_api, category, child_category
):
    result = await query_public_api(CATEGORIES_QUERY)
    ids = [i["id"] for i in result["data"]["categories"]]
    assert str(category.id) in ids
    assert str(child_category.id) not in ids


@pytest.mark.asyncio
async def test_categories_query_resolver_aggregates_categories_stats(
    query_public_api, category, child_category
):
    await category.update(threads=1, posts=2)
    await child_category.update(threads=2, posts=3)

    result = await query_public_api(CATEGORIES_QUERY)
    categories = {i["id"]: i for i in result["data"]["categories"]}
    assert categories[str(category.id)] == {
        "id": str(category.id),
        "threads": 3,
        "posts": 5,
    }


CATEGORY_QUERY = """
    query GetCategory($category: ID!) {
        category(id: $category) {
            id
            threads
            posts
        }
    }
"""


@pytest.mark.asyncio
async def test_category_query_resolves_by_id(query_public_api, category):
    result = await query_public_api(CATEGORY_QUERY, {"category": str(category.id)})
    assert result["data"]["category"]["id"] == str(category.id)


@pytest.mark.asyncio
async def test_category_query_stats_resolve_to_aggregated_values(
    query_public_api, category, child_category
):
    await category.update(threads=1, posts=2)
    await child_category.update(threads=2, posts=3)

    result = await query_public_api(CATEGORY_QUERY, {"category": str(category.id)})
    data = result["data"]["category"]
    assert data["id"] == str(category.id)
    assert data["threads"] == 3
    assert data["posts"] == 5


@pytest.mark.asyncio
async def test_category_query_resolves_to_none_for_non_existing_category(
    query_public_api, category
):
    result = await query_public_api(
        CATEGORY_QUERY, {"category": str(category.id * 1000)}
    )
    assert result["data"]["category"] is None
