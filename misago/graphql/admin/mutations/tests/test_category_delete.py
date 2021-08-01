import pytest

from .....categories.get import get_all_categories
from .....categories.models import Category
from .....threads.models import Post, Thread

CATEGORY_DELETE_MUTATION = """
    mutation CategoryDelete(
        $category: ID!, $moveChildrenTo: ID, $moveThreadsTo: ID
    ) {
        categoryDelete(
            category: $category,
            moveThreadsTo: $moveThreadsTo,
            moveChildrenTo: $moveChildrenTo
        ) {
            errors {
                location
                type
            }
            deleted
        }
    }
"""


@pytest.mark.asyncio
async def test_category_delete_mutation_deletes_category_with_its_children(
    query_admin_api, category, child_category
):
    variables = {"category": str(category.id)}
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["errors"]
    assert data["deleted"]

    db_categories = await get_all_categories()
    categories_ids = [c.id for c in db_categories]
    assert category.id not in categories_ids
    assert child_category.id not in categories_ids

    # Categories tree is valid
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 4),  # Sibling category
        (0, 5, 6),  # Closed category
    ]


@pytest.mark.asyncio
async def test_category_delete_mutation_deletes_category_but_moves_its_children(
    query_admin_api, category, child_category, sibling_category
):
    variables = {
        "category": str(category.id),
        "moveChildrenTo": str(sibling_category.id),
    }
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["errors"]
    assert data["deleted"]

    db_categories = await get_all_categories()
    categories_ids = [c.id for c in db_categories]
    assert category.id not in categories_ids
    assert child_category.id in categories_ids

    new_parent = await Category.query.one(id=sibling_category.id)
    assert new_parent.depth == 0
    assert new_parent.left == 3
    assert new_parent.right == 6

    updated_child = await Category.query.one(id=child_category.id)
    assert updated_child.depth == 1
    assert updated_child.left == 4
    assert updated_child.right == 5

    # Categories tree is valid
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 6),  # Sibling category
        (1, 4, 5),  # - Child category
        (0, 7, 8),  # Closed category
    ]


@pytest.mark.asyncio
async def test_category_delete_mutation_deletes_category_and_its_threads(
    query_admin_api, category, thread, post
):
    variables = {"category": str(category.id)}
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["errors"]
    assert data["deleted"]

    with pytest.raises(Thread.DoesNotExist):
        await thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        await post.refresh_from_db()

    db_categories = await get_all_categories()
    categories_ids = [c.id for c in db_categories]
    assert category.id not in categories_ids

    # Categories tree is valid
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 4),  # Sibling category
        (0, 5, 6),  # Closed category
    ]


@pytest.mark.asyncio
async def test_category_delete_but_move_children_mutation_keeps_children_threads(
    query_admin_api, category, child_category, sibling_category, thread, post
):
    await thread.update(category=child_category)
    await post.update(category=child_category)

    variables = {
        "category": str(category.id),
        "moveChildrenTo": str(sibling_category.id),
    }
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["errors"]
    assert data["deleted"]

    updated_thread = await thread.refresh_from_db()
    assert updated_thread.category_id == child_category.id

    updated_post = await post.refresh_from_db()
    assert updated_post.category_id == child_category.id


@pytest.mark.asyncio
async def test_category_delete_mutation_deletes_children_threads(
    query_admin_api, category, child_category, thread, post
):
    await thread.update(category=child_category)
    await post.update(category=child_category)

    variables = {
        "category": str(category.id),
    }
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["errors"]
    assert data["deleted"]

    with pytest.raises(Thread.DoesNotExist):
        await thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        await post.refresh_from_db()


@pytest.mark.asyncio
async def test_category_delete_but_move_threads_mutation_moves_children_threads(
    query_admin_api, category, child_category, sibling_category, thread, post
):
    await thread.update(category=child_category)
    await post.update(category=child_category)

    variables = {
        "category": str(category.id),
        "moveThreadsTo": str(sibling_category.id),
    }
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["errors"]
    assert data["deleted"]

    updated_thread = await thread.refresh_from_db()
    assert updated_thread.category_id == sibling_category.id

    updated_post = await post.refresh_from_db()
    assert updated_post.category_id == sibling_category.id


@pytest.mark.asyncio
async def test_category_delete_but_move_all_mutation_moves_category_threads(
    query_admin_api, category, child_category, sibling_category, thread, post
):
    variables = {
        "category": str(category.id),
        "moveChildrenTo": str(sibling_category.id),
        "moveThreadsTo": str(sibling_category.id),
    }
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["errors"]
    assert data["deleted"]

    updated_thread = await thread.refresh_from_db()
    assert updated_thread.category_id == sibling_category.id

    updated_post = await post.refresh_from_db()
    assert updated_post.category_id == sibling_category.id


@pytest.mark.asyncio
async def test_category_delete_but_move_all_mutation_keeps_children_threads(
    query_admin_api, category, child_category, sibling_category, thread, post
):
    await thread.update(category=child_category)
    await post.update(category=child_category)

    variables = {
        "category": str(category.id),
        "moveChildrenTo": str(sibling_category.id),
        "moveThreadsTo": str(sibling_category.id),
    }
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["errors"]
    assert data["deleted"]

    updated_thread = await thread.refresh_from_db()
    assert updated_thread.category_id == child_category.id

    updated_post = await post.refresh_from_db()
    assert updated_post.category_id == child_category.id


@pytest.mark.asyncio
async def test_category_delete_mutation_fails_if_category_id_is_invalid(
    query_admin_api, category
):
    variables = {
        "category": "invalid",
    }
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["deleted"]
    assert data["errors"] == [{"location": ["category"], "type": "type_error.integer"}]


@pytest.mark.asyncio
async def test_category_delete_mutation_fails_if_move_children_id_is_invalid(
    query_admin_api, category
):
    variables = {
        "category": str(category.id),
        "moveChildrenTo": "invalid",
    }
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["deleted"]
    assert data["errors"] == [
        {"location": ["moveChildrenTo"], "type": "type_error.integer"}
    ]


@pytest.mark.asyncio
async def test_category_delete_mutation_fails_if_move_threads_id_is_invalid(
    query_admin_api, category
):
    variables = {
        "category": str(category.id),
        "moveThreadsTo": "invalid",
    }
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["deleted"]
    assert data["errors"] == [
        {"location": ["moveThreadsTo"], "type": "type_error.integer"}
    ]


@pytest.mark.asyncio
async def test_category_delete_mutation_fails_if_threads_are_moved_to_deleted_category(
    query_admin_api, category
):
    variables = {
        "category": str(category.id),
        "moveThreadsTo": str(category.id),
    }
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["deleted"]
    assert data["errors"] == [
        {"location": ["moveThreadsTo"], "type": "value_error.category.invalid"}
    ]


@pytest.mark.asyncio
async def test_category_delete_mutation_fails_if_threads_are_moved_to_deleted_child(
    query_admin_api, category, child_category
):
    variables = {
        "category": str(category.id),
        "moveThreadsTo": str(child_category.id),
    }
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["deleted"]
    assert data["errors"] == [
        {"location": ["moveThreadsTo"], "type": "value_error.category.invalid"}
    ]


@pytest.mark.asyncio
async def test_category_delete_mutation_fails_if_children_are_moved_to_deleted_category(
    query_admin_api, category
):
    variables = {
        "category": str(category.id),
        "moveChildrenTo": str(category.id),
    }
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["deleted"]
    assert data["errors"] == [
        {"location": ["moveChildrenTo"], "type": "value_error.category.invalid"}
    ]


@pytest.mark.asyncio
async def test_category_delete_mutation_fails_if_children_are_moved_to_child_category(
    query_admin_api, sibling_category, child_category
):
    variables = {
        "category": str(sibling_category.id),
        "moveChildrenTo": str(child_category.id),
    }
    result = await query_admin_api(CATEGORY_DELETE_MUTATION, variables)
    data = result["data"]["categoryDelete"]
    assert not data["deleted"]
    assert data["errors"] == [
        {"location": ["moveChildrenTo"], "type": "value_error.category.invalid"}
    ]


@pytest.mark.asyncio
async def test_category_delete_mutation_requires_admin_auth(query_admin_api, category):
    variables = {
        "category": str(category.id),
    }
    result = await query_admin_api(
        CATEGORY_DELETE_MUTATION, variables, include_auth=False, expect_error=True
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None
