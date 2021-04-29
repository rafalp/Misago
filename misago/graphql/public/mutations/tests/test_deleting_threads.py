import pytest

from .....errors import ErrorsList
from .....threads.models import Thread
from ..deletethreads import resolve_delete_threads


@pytest.mark.asyncio
async def test_delete_threads_mutation_deletes_threads(moderator_graphql_info, thread):
    data = await resolve_delete_threads(
        None,
        moderator_graphql_info,
        input={"threads": [str(thread.id)]},
    )

    assert "errors" not in data
    assert data["deleted"] == [thread.id]

    with pytest.raises(Thread.DoesNotExist):
        await thread.refresh_from_db()


@pytest.mark.asyncio
async def test_delete_threads_mutation_fails_if_user_is_not_authorized(
    graphql_info, thread
):
    data = await resolve_delete_threads(
        None,
        graphql_info,
        input={"threads": [str(thread.id)]},
    )

    assert data["errors"].get_errors_locations() == [
        "threads.0",
        ErrorsList.ROOT_LOCATION,
    ]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
        "auth_error.not_authorized",
    ]
    assert data["deleted"] == []
    assert await thread.refresh_from_db()


@pytest.mark.asyncio
async def test_delete_threads_mutation_fails_if_user_is_not_moderator(
    user_graphql_info, thread
):
    data = await resolve_delete_threads(
        None,
        user_graphql_info,
        input={"threads": [str(thread.id)]},
    )

    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
    ]
    assert data["deleted"] == []
    assert await thread.refresh_from_db()


@pytest.mark.asyncio
async def test_delete_threads_mutation_fails_if_thread_id_is_invalid(
    moderator_graphql_info,
):
    data = await resolve_delete_threads(
        None,
        moderator_graphql_info,
        input={"threads": ["invalid"]},
    )

    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]
    assert data["deleted"] == []


@pytest.mark.asyncio
async def test_delete_threads_mutation_fails_if_thread_doesnt_exist(
    moderator_graphql_info,
):
    data = await resolve_delete_threads(
        None,
        moderator_graphql_info,
        input={"threads": ["4000"]},
    )

    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["value_error.thread.not_exists"]
    assert data["deleted"] == []


@pytest.mark.asyncio
async def test_delete_threads_mutation_with_threads_errors_still_deletes_valid_threads(
    moderator_graphql_info, thread
):
    data = await resolve_delete_threads(
        None,
        moderator_graphql_info,
        input={"threads": ["4000", str(thread.id)]},
    )

    assert data["errors"].get_errors_locations() == ["threads.0"]
    assert data["errors"].get_errors_types() == ["value_error.thread.not_exists"]
    assert data["deleted"] == [thread.id]

    with pytest.raises(Thread.DoesNotExist):
        await thread.refresh_from_db()
