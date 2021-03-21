import pytest

from .....categories.get import get_all_categories, get_category_by_id
from .....threads.get import get_post_by_id, get_thread_by_id
from .....threads.update import update_post, update_thread
from ..deletecategory import resolve_delete_category


@pytest.mark.asyncio
async def test_delete_category_mutation_deletes_category_with_its_children(
    admin_graphql_info, category, child_category
):
    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category=str(category.id),
    )

    assert not data.get("errors")
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
async def test_delete_category_mutation_deletes_category_but_moves_its_children(
    admin_graphql_info, category, child_category, sibling_category
):
    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        move_children_to=str(sibling_category.id),
    )

    assert not data.get("errors")
    assert data["deleted"]

    db_categories = await get_all_categories()
    categories_ids = [c.id for c in db_categories]
    assert category.id not in categories_ids
    assert child_category.id in categories_ids

    new_parent = await get_category_by_id(sibling_category.id)
    assert new_parent.depth == 0
    assert new_parent.left == 3
    assert new_parent.right == 6

    updated_child = await get_category_by_id(child_category.id)
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
async def test_delete_category_mutation_deletes_category_and_its_threads(
    admin_graphql_info, category, thread, post
):
    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category=str(category.id),
    )

    assert not data.get("errors")
    assert data["deleted"]

    assert await get_thread_by_id(thread.id) is None
    assert await get_post_by_id(post.id) is None

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
async def test_delete_category_but_move_children_mutation_keeps_children_threads(
    admin_graphql_info, category, child_category, sibling_category, thread, post
):
    await update_thread(thread, category=child_category)
    await update_post(post, category=child_category)

    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        move_children_to=str(sibling_category.id),
    )

    assert not data.get("errors")
    assert data["deleted"]

    updated_thread = await get_thread_by_id(thread.id)
    assert updated_thread.category_id == child_category.id

    updated_post = await get_post_by_id(post.id)
    assert updated_post.category_id == child_category.id


@pytest.mark.asyncio
async def test_delete_category_mutation_deletes_children_threads(
    admin_graphql_info, category, child_category, thread, post
):
    await update_thread(thread, category=child_category)
    await update_post(post, category=child_category)

    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category=str(category.id),
    )

    assert not data.get("errors")
    assert data["deleted"]

    assert await get_thread_by_id(thread.id) is None
    assert await get_post_by_id(post.id) is None


@pytest.mark.asyncio
async def test_delete_category_but_move_threads_mutation_moves_children_threads(
    admin_graphql_info, category, child_category, sibling_category, thread, post
):
    await update_thread(thread, category=child_category)
    await update_post(post, category=child_category)

    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        move_threads_to=str(sibling_category.id),
    )

    assert not data.get("errors")
    assert data["deleted"]

    updated_thread = await get_thread_by_id(thread.id)
    assert updated_thread.category_id == sibling_category.id

    updated_post = await get_post_by_id(post.id)
    assert updated_post.category_id == sibling_category.id


@pytest.mark.asyncio
async def test_delete_category_but_move_all_mutation_moves_category_threads(
    admin_graphql_info, category, child_category, sibling_category, thread, post
):
    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        move_children_to=str(sibling_category.id),
        move_threads_to=str(sibling_category.id),
    )

    assert not data.get("errors")
    assert data["deleted"]

    updated_thread = await get_thread_by_id(thread.id)
    assert updated_thread.category_id == sibling_category.id

    updated_post = await get_post_by_id(post.id)
    assert updated_post.category_id == sibling_category.id


@pytest.mark.asyncio
async def test_delete_category_but_move_all_mutation_keeps_children_threads(
    admin_graphql_info, category, child_category, sibling_category, thread, post
):
    await update_thread(thread, category=child_category)
    await update_post(post, category=child_category)

    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        move_children_to=str(sibling_category.id),
        move_threads_to=str(sibling_category.id),
    )

    assert not data.get("errors")
    assert data["deleted"]

    updated_thread = await get_thread_by_id(thread.id)
    assert updated_thread.category_id == child_category.id

    updated_post = await get_post_by_id(post.id)
    assert updated_post.category_id == child_category.id


@pytest.mark.asyncio
async def test_delete_category_mutation_fails_if_category_id_is_invalid(
    admin_graphql_info, category
):
    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category="invalid",
    )

    assert not data["deleted"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["category"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_delete_category_mutation_fails_if_move_children_id_is_invalid(
    admin_graphql_info, category
):
    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        move_children_to=str("invalid"),
    )

    assert not data["deleted"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["moveChildrenTo"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_delete_category_mutation_fails_if_move_threads_id_is_invalid(
    admin_graphql_info, category
):
    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        move_threads_to=str("invalid"),
    )

    assert not data["deleted"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["moveThreadsTo"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_delete_category_mutation_fails_if_threads_are_moved_to_deleted_category(
    admin_graphql_info, category
):
    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        move_threads_to=str(category.id),
    )

    assert not data["deleted"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["moveThreadsTo"]
    assert data["errors"].get_errors_types() == ["value_error.category.invalid"]


@pytest.mark.asyncio
async def test_delete_category_mutation_fails_if_threads_are_moved_to_deleted_child(
    admin_graphql_info, category, child_category
):
    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        move_threads_to=str(child_category.id),
    )

    assert not data["deleted"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["moveThreadsTo"]
    assert data["errors"].get_errors_types() == ["value_error.category.invalid"]


@pytest.mark.asyncio
async def test_delete_category_mutation_fails_if_children_are_moved_to_deleted_category(
    admin_graphql_info, category
):
    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        move_children_to=str(category.id),
    )

    assert not data["deleted"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["moveChildrenTo"]
    assert data["errors"].get_errors_types() == ["value_error.category.invalid"]


@pytest.mark.asyncio
async def test_delete_category_mutation_fails_if_children_are_moved_to_child_category(
    admin_graphql_info, sibling_category, child_category
):
    data = await resolve_delete_category(
        None,
        admin_graphql_info,
        category=str(sibling_category.id),
        move_children_to=str(child_category.id),
    )

    assert not data["deleted"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["moveChildrenTo"]
    assert data["errors"].get_errors_types() == ["value_error.category.invalid"]
