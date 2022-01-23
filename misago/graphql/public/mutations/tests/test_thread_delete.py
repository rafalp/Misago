import pytest

from .....errors import ErrorsList
from .....threads.models import Thread

THREAD_DELETE_MUTATION = """
    mutation ThreadDelete($thread: ID!) {
        threadDelete(thread: $thread) {
            deleted
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_thread_delete_mutation_deletes_thread(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        THREAD_DELETE_MUTATION,
        {"thread": str(thread.id)},
        auth=moderator,
    )

    assert result["data"]["threadDelete"] == {
        "deleted": True,
        "errors": None,
    }

    with pytest.raises(Thread.DoesNotExist):
        await thread.refresh_from_db()


@pytest.mark.asyncio
async def test_thread_delete_mutation_fails_if_user_is_not_authorized(
    query_public_api, thread
):
    result = await query_public_api(
        THREAD_DELETE_MUTATION,
        {"thread": str(thread.id)},
    )

    assert result["data"]["threadDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "thread",
                "type": "auth_error.not_moderator",
            },
            {
                "location": ErrorsList.ROOT_LOCATION,
                "type": "auth_error.not_authorized",
            },
        ],
    }

    await thread.refresh_from_db()


@pytest.mark.asyncio
async def test_thread_delete_mutation_fails_if_user_is_not_moderator(
    query_public_api, user, thread
):
    result = await query_public_api(
        THREAD_DELETE_MUTATION,
        {"thread": str(thread.id)},
        auth=user,
    )

    assert result["data"]["threadDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "thread",
                "type": "auth_error.not_moderator",
            },
        ],
    }

    await thread.refresh_from_db()


@pytest.mark.asyncio
async def test_thread_delete_mutation_fails_if_thread_id_is_invalid(
    query_public_api, moderator
):
    result = await query_public_api(
        THREAD_DELETE_MUTATION,
        {"thread": "invalid"},
        auth=moderator,
    )

    assert result["data"]["threadDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "thread",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_thread_delete_mutation_fails_if_thread_doesnt_exist(
    query_public_api, moderator
):
    result = await query_public_api(
        THREAD_DELETE_MUTATION,
        {"thread": "4000"},
        auth=moderator,
    )

    assert result["data"]["threadDelete"] == {
        "deleted": False,
        "errors": [
            {
                "location": "thread",
                "type": "value_error.thread.not_found",
            },
        ],
    }
