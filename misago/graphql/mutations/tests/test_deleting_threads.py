import pytest

from ....errors import ErrorsList
from ....threads.get import get_thread_by_id
from ..deletethreads import resolve_delete_threads


@pytest.mark.asyncio
async def test_delete_threads_mutation_deletes_threads(moderator_graphql_info, thread):
    data = await resolve_delete_threads(
        None, moderator_graphql_info, input={"threads": [str(thread.id)]},
    )

    assert not data.get("errors")
    assert await get_thread_by_id(thread.id) is None


@pytest.mark.asyncio
async def test_delete_threads_mutation_fails_if_user_is_not_authorized(
    graphql_info, thread
):
    data = await resolve_delete_threads(
        None, graphql_info, input={"threads": [str(thread.id)]},
    )

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
async def test_delete_threads_mutation_fails_if_user_is_not_moderator(
    user_graphql_info, thread
):
    data = await resolve_delete_threads(
        None, user_graphql_info, input={"threads": [str(thread.id)]},
    )

    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
    ]


@pytest.mark.asyncio
async def test_delete_threads_mutation_fails_if_thread_id_is_invalid(
    moderator_graphql_info,
):
    data = await resolve_delete_threads(
        None, moderator_graphql_info, input={"threads": ["invalid"]},
    )

    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_delete_threads_mutation_fails_if_thread_doesnt_exist(
    moderator_graphql_info,
):
    data = await resolve_delete_threads(
        None, moderator_graphql_info, input={"threads": ["4000"]},
    )

    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["value_error.thread_does_not_exist"]
