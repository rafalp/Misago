import pytest

from ....errors import ErrorsList
from ....threads.get import get_thread_by_id
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

    assert not data.get("errors")
    assert data.get("threads")
    assert data["threads"] == [await get_thread_by_id(data["threads"][0].id)]
    assert data["threads"][0].category_id == sibling_category.id


@pytest.mark.asyncio
async def test_move_threads_mutation_fails_if_user_is_not_authorized(
    graphql_info, thread, sibling_category
):
    data = await resolve_move_threads(
        None,
        graphql_info,
        input={"threads": [str(thread.id)], "category": str(sibling_category.id)},
    )

    assert data.get("threads")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == [
        "threads.0",
        ErrorsList.ROOT_LOCATION,
    ]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
        "auth_error.not_authorized",
    ]


@pytest.mark.asyncio
async def test_move_threads_mutation_fails_if_user_is_not_moderator(
    user_graphql_info, thread, sibling_category
):
    data = await resolve_move_threads(
        None,
        user_graphql_info,
        input={"threads": [str(thread.id)], "category": str(sibling_category.id)},
    )

    assert data.get("threads")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
    ]


@pytest.mark.asyncio
async def test_move_threads_mutation_fails_if_thread_id_is_invalid(
    moderator_graphql_info, sibling_category
):
    data = await resolve_move_threads(
        None,
        moderator_graphql_info,
        input={"threads": ["invalid"], "category": str(sibling_category.id)},
    )

    assert not data.get("threads")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_move_threads_mutation_fails_if_thread_doesnt_exist(
    moderator_graphql_info, sibling_category
):
    data = await resolve_move_threads(
        None,
        moderator_graphql_info,
        input={"threads": ["4000"], "category": str(sibling_category.id)},
    )

    assert not data.get("threads")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["value_error.thread_does_not_exist"]


@pytest.mark.asyncio
async def test_move_threads_mutation_fails_if_category_id_is_invalid(
    moderator_graphql_info, thread
):
    data = await resolve_move_threads(
        None,
        moderator_graphql_info,
        input={"threads": [str(thread.id)], "category": "invalid"},
    )

    assert data.get("threads")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["category"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_move_threads_mutation_fails_if_category_doesnt_exist(
    moderator_graphql_info, thread
):
    data = await resolve_move_threads(
        None,
        moderator_graphql_info,
        input={"threads": [str(thread.id)], "category": "1000"},
    )

    assert data.get("threads")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["category"]
    assert data["errors"].get_errors_types() == ["value_error.category_does_not_exist"]
