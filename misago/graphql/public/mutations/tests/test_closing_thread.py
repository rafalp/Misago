import pytest

from .....errors import ErrorsList
from .....threads.get import get_thread_by_id
from ..closethread import resolve_close_thread


@pytest.mark.asyncio
async def test_close_thread_mutation_closes_thread(moderator_graphql_info, thread):
    data = await resolve_close_thread(
        None,
        moderator_graphql_info,
        input={"thread": str(thread.id), "isClosed": True},
    )

    assert not data.get("errors")
    assert data.get("thread")
    assert data["thread"] == await get_thread_by_id(data["thread"].id)
    assert data["thread"].is_closed


@pytest.mark.asyncio
async def test_close_thread_mutation_opens_thread(
    moderator_graphql_info, closed_thread
):
    data = await resolve_close_thread(
        None,
        moderator_graphql_info,
        input={"thread": str(closed_thread.id), "isClosed": False},
    )

    assert not data.get("errors")
    assert data.get("thread")
    assert data["thread"] == await get_thread_by_id(data["thread"].id)
    assert not data["thread"].is_closed


@pytest.mark.asyncio
async def test_close_thread_mutation_fails_if_user_is_not_authorized(
    graphql_info, thread
):
    data = await resolve_close_thread(
        None, graphql_info, input={"thread": str(thread.id), "isClosed": True},
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread", ErrorsList.ROOT_LOCATION]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
        "auth_error.not_authorized",
    ]


@pytest.mark.asyncio
async def test_close_thread_mutation_fails_if_user_is_not_moderator(
    user_graphql_info, thread
):
    data = await resolve_close_thread(
        None, user_graphql_info, input={"thread": str(thread.id), "isClosed": True},
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
    ]


@pytest.mark.asyncio
async def test_close_thread_mutation_fails_if_thread_id_is_invalid(
    moderator_graphql_info,
):
    data = await resolve_close_thread(
        None, moderator_graphql_info, input={"thread": "invalid", "isClosed": True},
    )

    assert not data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_close_thread_mutation_fails_if_thread_doesnt_exist(
    moderator_graphql_info,
):
    data = await resolve_close_thread(
        None, moderator_graphql_info, input={"thread": "4000", "isClosed": True},
    )

    assert not data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["value_error.thread.not_exists"]
