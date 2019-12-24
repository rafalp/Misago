import pytest

from ....errors import ErrorsList
from ....threads.get import get_thread_by_id
from ..closethreads import resolve_close_threads


@pytest.mark.asyncio
async def test_close_threads_mutation_closes_threads(moderator_graphql_info, thread):
    data = await resolve_close_threads(
        None,
        moderator_graphql_info,
        input={"threads": [str(thread.id)], "isClosed": True},
    )

    assert not data.get("errors")
    assert data.get("threads")
    assert data["threads"] == [await get_thread_by_id(data["threads"][0].id)]
    assert data["threads"][0].is_closed


@pytest.mark.asyncio
async def test_close_threads_mutation_opens_threads(
    moderator_graphql_info, closed_thread
):
    data = await resolve_close_threads(
        None,
        moderator_graphql_info,
        input={"threads": [str(closed_thread.id)], "isClosed": False},
    )

    assert not data.get("errors")
    assert data.get("threads")
    assert data["threads"] == [await get_thread_by_id(data["threads"][0].id)]
    assert not data["threads"][0].is_closed


@pytest.mark.asyncio
async def test_close_threads_mutation_fails_if_user_is_not_authorized(
    graphql_info, thread
):
    data = await resolve_close_threads(
        None, graphql_info, input={"threads": [str(thread.id)], "isClosed": True},
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
async def test_close_threads_mutation_fails_if_user_is_not_moderator(
    user_graphql_info, thread
):
    data = await resolve_close_threads(
        None, user_graphql_info, input={"threads": [str(thread.id)], "isClosed": True},
    )

    assert data.get("threads")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
    ]


@pytest.mark.asyncio
async def test_close_threads_mutation_fails_if_threads_id_list_is_empty(
    moderator_graphql_info,
):
    data = await resolve_close_threads(
        None, moderator_graphql_info, input={"threads": [], "isClosed": True},
    )

    assert not data.get("threads")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["threads"]
    assert data["errors"].get_errors_types() == ["value_error.list.min_items"]


@pytest.mark.asyncio
async def test_close_threads_mutation_fails_if_threads_id_list_is_too_long(
    moderator_graphql_info,
):
    data = await resolve_close_threads(
        None,
        moderator_graphql_info,
        input={"threads": list(range(100)), "isClosed": True},
    )

    assert not data.get("threads")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["threads"]
    assert data["errors"].get_errors_types() == ["value_error.list.max_items"]


@pytest.mark.asyncio
async def test_close_threads_mutation_fails_if_thread_id_is_invalid(
    moderator_graphql_info,
):
    data = await resolve_close_threads(
        None, moderator_graphql_info, input={"threads": ["invalid"], "isClosed": True},
    )

    assert not data.get("threads")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_close_threads_mutation_fails_if_thread_doesnt_exist(
    moderator_graphql_info,
):
    data = await resolve_close_threads(
        None, moderator_graphql_info, input={"threads": ["4000"], "isClosed": True},
    )

    assert not data.get("threads")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["value_error.thread_does_not_exist"]
