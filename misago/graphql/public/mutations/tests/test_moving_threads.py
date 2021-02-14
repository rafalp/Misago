import pytest

from .....errors import ErrorsList
from .....threads.get import get_thread_by_id
from ..movethreads import resolve_move_threads


@pytest.mark.asyncio
async def test_move_threads_mutation_moves_threads(
    moderator_graphql_info, thread, sibling_category
):
    data = await resolve_move_threads(
        None,
        moderator_graphql_info,
        input={"threads": [str(thread.id)], "category": str(sibling_category.id)},
    )

    assert "errors" not in data
    assert data["threads"] == [await get_thread_by_id(data["threads"][0].id)]
    assert data["threads"][0].category_id == sibling_category.id
    assert data["updated"]


@pytest.mark.asyncio
async def test_move_threads_mutation_fails_if_user_is_not_authorized(
    graphql_info, thread, sibling_category
):
    data = await resolve_move_threads(
        None,
        graphql_info,
        input={"threads": [str(thread.id)], "category": str(sibling_category.id)},
    )

    assert data["errors"].get_errors_locations() == [
        "threads.0",
        ErrorsList.ROOT_LOCATION,
    ]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
        "auth_error.not_authorized",
    ]
    assert data["threads"][0].category_id == thread.category_id
    assert not data["updated"]


@pytest.mark.asyncio
async def test_move_threads_mutation_fails_if_user_is_not_moderator(
    user_graphql_info, thread, sibling_category
):
    data = await resolve_move_threads(
        None,
        user_graphql_info,
        input={"threads": [str(thread.id)], "category": str(sibling_category.id)},
    )

    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
    ]
    assert data["threads"][0].category_id == thread.category_id
    assert not data["updated"]


@pytest.mark.asyncio
async def test_move_threads_mutation_fails_if_thread_id_is_invalid(
    moderator_graphql_info, sibling_category
):
    data = await resolve_move_threads(
        None,
        moderator_graphql_info,
        input={"threads": ["invalid"], "category": str(sibling_category.id)},
    )

    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]
    assert not data["threads"]
    assert not data["updated"]


@pytest.mark.asyncio
async def test_move_threads_mutation_fails_if_thread_doesnt_exist(
    moderator_graphql_info, sibling_category
):
    data = await resolve_move_threads(
        None,
        moderator_graphql_info,
        input={"threads": ["4000"], "category": str(sibling_category.id)},
    )

    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["value_error.thread.not_exists"]
    assert not data["threads"]
    assert not data["updated"]


@pytest.mark.asyncio
async def test_move_threads_mutation_fails_if_category_id_is_invalid(
    moderator_graphql_info, thread
):
    data = await resolve_move_threads(
        None,
        moderator_graphql_info,
        input={"threads": [str(thread.id)], "category": "invalid"},
    )

    assert data["errors"].get_errors_locations() == ["category"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]
    assert data["threads"][0].category_id == thread.category_id
    assert not data["updated"]


@pytest.mark.asyncio
async def test_move_threads_mutation_fails_if_category_doesnt_exist(
    moderator_graphql_info, thread
):
    data = await resolve_move_threads(
        None,
        moderator_graphql_info,
        input={"threads": [str(thread.id)], "category": "1000"},
    )

    assert data["errors"].get_errors_locations() == ["category"]
    assert data["errors"].get_errors_types() == ["value_error.category.not_exists"]
    assert data["threads"][0].category_id == thread.category_id
    assert not data["updated"]


@pytest.mark.asyncio
async def test_move_threads_mutation_with_threads_errors_still_updates_valid_threads(
    moderator_graphql_info, thread, sibling_category
):
    data = await resolve_move_threads(
        None,
        moderator_graphql_info,
        input={
            "threads": ["4000", str(thread.id)],
            "category": str(sibling_category.id),
        },
    )

    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["value_error.thread.not_exists"]
    assert data["threads"][0].category_id == sibling_category.id
    assert data["updated"]
