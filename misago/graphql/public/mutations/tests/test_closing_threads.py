import pytest

from .....errors import ErrorsList
from ..closethreads import resolve_close_threads


@pytest.mark.asyncio
async def test_close_threads_mutation_closes_threads(moderator_graphql_info, thread):
    data = await resolve_close_threads(
        None,
        moderator_graphql_info,
        input={"threads": [str(thread.id)], "isClosed": True},
    )

    assert "errors" not in data
    assert data["threads"] == [await data["threads"][0].refresh_from_db()]
    assert data["threads"][0].is_closed
    assert data["updated"]


@pytest.mark.asyncio
async def test_close_threads_mutation_opens_threads(
    moderator_graphql_info, closed_thread
):
    data = await resolve_close_threads(
        None,
        moderator_graphql_info,
        input={"threads": [str(closed_thread.id)], "isClosed": False},
    )

    assert "errors" not in data
    assert data["threads"] == [await data["threads"][0].refresh_from_db()]
    assert not data["threads"][0].is_closed
    assert data["updated"]


@pytest.mark.asyncio
async def test_close_threads_mutation_fails_if_user_is_not_authorized(
    graphql_info, thread
):
    data = await resolve_close_threads(
        None,
        graphql_info,
        input={"threads": [str(thread.id)], "isClosed": True},
    )

    assert data["errors"].get_errors_locations() == [
        "threads.0",
        ErrorsList.ROOT_LOCATION,
    ]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
        "auth_error.not_authorized",
    ]
    assert not data["threads"][0].is_closed
    assert not data["updated"]


@pytest.mark.asyncio
async def test_close_threads_mutation_fails_if_user_is_not_moderator(
    user_graphql_info, thread
):
    data = await resolve_close_threads(
        None,
        user_graphql_info,
        input={"threads": [str(thread.id)], "isClosed": True},
    )

    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
    ]
    assert not data["threads"][0].is_closed
    assert not data["updated"]


@pytest.mark.asyncio
async def test_close_threads_mutation_fails_if_thread_id_is_invalid(
    moderator_graphql_info,
):
    data = await resolve_close_threads(
        None,
        moderator_graphql_info,
        input={"threads": ["invalid"], "isClosed": True},
    )

    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]
    assert not data["threads"]
    assert not data["updated"]


@pytest.mark.asyncio
async def test_close_threads_mutation_fails_if_thread_doesnt_exist(
    moderator_graphql_info,
):
    data = await resolve_close_threads(
        None,
        moderator_graphql_info,
        input={"threads": ["4000"], "isClosed": True},
    )

    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["value_error.thread.not_exists"]
    assert not data["threads"]
    assert not data["updated"]


@pytest.mark.asyncio
async def test_close_threads_mutation_with_threads_errors_still_updates_valid_threads(
    moderator_graphql_info, thread
):
    data = await resolve_close_threads(
        None,
        moderator_graphql_info,
        input={"threads": ["4000", str(thread.id)], "isClosed": True},
    )

    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["value_error.thread.not_exists"]
    assert len(data["threads"]) == 1
    assert data["threads"][0].is_closed
    assert data["updated"]
