import pytest

from .....errors import ErrorsList
from .....threads.models import Thread

DELETE_THREADS_MUTATION = """
    mutation DeleteThreads($input: BulkDeleteThreadsInput!) {
        deleteThreads(input: $input) {
            deleted
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_delete_threads_mutation_deletes_threads(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        DELETE_THREADS_MUTATION,
        {"input": {"threads": [str(thread.id)]}},
        auth=moderator,
    )

    assert result["data"]["deleteThreads"] == {
        "deleted": [str(thread.id)],
        "errors": None,
    }

    with pytest.raises(Thread.DoesNotExist):
        await thread.refresh_from_db()


@pytest.mark.asyncio
async def test_delete_threads_mutation_fails_if_user_is_not_authorized(
    query_public_api, thread
):
    result = await query_public_api(
        DELETE_THREADS_MUTATION,
        {"input": {"threads": [str(thread.id)]}},
    )

    assert result["data"]["deleteThreads"] == {
        "deleted": [],
        "errors": [
            {
                "location": "threads.0",
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
async def test_delete_threads_mutation_fails_if_user_is_not_moderator(
    query_public_api, user, thread
):
    result = await query_public_api(
        DELETE_THREADS_MUTATION,
        {"input": {"threads": [str(thread.id)]}},
        auth=user,
    )

    assert result["data"]["deleteThreads"] == {
        "deleted": [],
        "errors": [
            {
                "location": "threads.0",
                "type": "auth_error.not_moderator",
            },
        ],
    }

    await thread.refresh_from_db()


@pytest.mark.asyncio
async def test_delete_threads_mutation_fails_if_thread_id_is_invalid(
    query_public_api, moderator
):
    result = await query_public_api(
        DELETE_THREADS_MUTATION,
        {"input": {"threads": ["invalid"]}},
        auth=moderator,
    )

    assert result["data"]["deleteThreads"] == {
        "deleted": [],
        "errors": [
            {
                "location": "threads.0",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_delete_threads_mutation_fails_if_thread_doesnt_exist(
    query_public_api, moderator
):
    result = await query_public_api(
        DELETE_THREADS_MUTATION,
        {"input": {"threads": ["4000"]}},
        auth=moderator,
    )

    assert result["data"]["deleteThreads"] == {
        "deleted": [],
        "errors": [
            {
                "location": "threads.0",
                "type": "value_error.thread.not_exists",
            },
        ],
    }


@pytest.mark.asyncio
async def test_delete_threads_mutation_with_threads_errors_still_deletes_valid_threads(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        DELETE_THREADS_MUTATION,
        {"input": {"threads": ["4000", str(thread.id)]}},
        auth=moderator,
    )

    assert result["data"]["deleteThreads"] == {
        "deleted": [str(thread.id)],
        "errors": [
            {
                "location": "threads.0",
                "type": "value_error.thread.not_exists",
            },
        ],
    }

    with pytest.raises(Thread.DoesNotExist):
        await thread.refresh_from_db()
