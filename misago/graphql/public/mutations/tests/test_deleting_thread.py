import pytest

from .....errors import ErrorsList
from .....threads.get import get_thread_by_id
from ..deletethread import resolve_delete_thread


@pytest.mark.asyncio
async def test_delete_thread_mutation_deletes_thread(moderator_graphql_info, thread):
    data = await resolve_delete_thread(
        None, moderator_graphql_info, input={"thread": str(thread.id)},
    )

    assert not data.get("errors")
    assert data["deleted"] == [thread.id]
    assert await get_thread_by_id(thread.id) is None


@pytest.mark.asyncio
async def test_delete_thread_mutation_fails_if_user_is_not_authorized(
    graphql_info, thread
):
    data = await resolve_delete_thread(
        None, graphql_info, input={"thread": str(thread.id)},
    )

    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread", ErrorsList.ROOT_LOCATION]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
        "auth_error.not_authorized",
    ]
    assert data["deleted"] == []


@pytest.mark.asyncio
async def test_delete_thread_mutation_fails_if_user_is_not_moderator(
    user_graphql_info, thread
):
    data = await resolve_delete_thread(
        None, user_graphql_info, input={"thread": str(thread.id)},
    )

    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
    ]
    assert data["deleted"] == []


@pytest.mark.asyncio
async def test_delete_thread_mutation_fails_if_thread_id_is_invalid(
    moderator_graphql_info,
):
    data = await resolve_delete_thread(
        None, moderator_graphql_info, input={"thread": "invalid"},
    )

    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]
    assert data["deleted"] == []


@pytest.mark.asyncio
async def test_delete_thread_mutation_fails_if_thread_doesnt_exist(
    moderator_graphql_info,
):
    data = await resolve_delete_thread(
        None, moderator_graphql_info, input={"thread": "4000"},
    )

    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["value_error.thread.not_exists"]
    assert data["deleted"] == []
