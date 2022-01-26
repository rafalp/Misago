import pytest

from .....errors import ErrorsList
from .....threads.models import Thread

THREADS_BULK_DELETE_MUTATION = """
    mutation ThreadsBulkDelete($threads: [ID!]!) {
        threadsBulkDelete(threads: $threads) {
            deleted
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_threads_bulk_delete_mutation_deletes_threads(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        THREADS_BULK_DELETE_MUTATION,
        {"threads": [str(thread.id)]},
        auth=moderator,
    )

    assert result["data"]["threadsBulkDelete"] == {
        "deleted": [str(thread.id)],
        "errors": None,
    }

    with pytest.raises(Thread.DoesNotExist):
        await thread.fetch_from_db()


@pytest.mark.asyncio
async def test_threads_bulk_delete_mutation_fails_if_user_is_not_authenticated(
    query_public_api, thread
):
    result = await query_public_api(
        THREADS_BULK_DELETE_MUTATION,
        {"threads": [str(thread.id)]},
    )

    assert result["data"]["threadsBulkDelete"] == {
        "deleted": [],
        "errors": [
            {
                "location": "threads.0",
                "type": "auth_error.not_moderator",
            },
            {
                "location": ErrorsList.ROOT_LOCATION,
                "type": "auth_error.not_authenticated",
            },
        ],
    }

    await thread.fetch_from_db()


@pytest.mark.asyncio
async def test_threads_bulk_delete_mutation_fails_if_user_is_not_moderator(
    query_public_api, user, thread
):
    result = await query_public_api(
        THREADS_BULK_DELETE_MUTATION,
        {"threads": [str(thread.id)]},
        auth=user,
    )

    assert result["data"]["threadsBulkDelete"] == {
        "deleted": [],
        "errors": [
            {
                "location": "threads.0",
                "type": "auth_error.not_moderator",
            },
        ],
    }

    await thread.fetch_from_db()


@pytest.mark.asyncio
async def test_threads_bulk_delete_mutation_fails_if_thread_id_is_invalid(
    query_public_api, moderator
):
    result = await query_public_api(
        THREADS_BULK_DELETE_MUTATION,
        {"threads": ["invalid"]},
        auth=moderator,
    )

    assert result["data"]["threadsBulkDelete"] == {
        "deleted": [],
        "errors": [
            {
                "location": "threads.0",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_threads_bulk_delete_mutation_fails_if_thread_doesnt_exist(
    query_public_api, moderator
):
    result = await query_public_api(
        THREADS_BULK_DELETE_MUTATION,
        {"threads": ["4000"]},
        auth=moderator,
    )

    assert result["data"]["threadsBulkDelete"] == {
        "deleted": [],
        "errors": [
            {
                "location": "threads.0",
                "type": "thread_error.not_found",
            },
        ],
    }


@pytest.mark.asyncio
async def test_threads_bulk_delete_mutation_with_threads_errors_still_deletes_valid_threads(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        THREADS_BULK_DELETE_MUTATION,
        {"threads": ["4000", str(thread.id)]},
        auth=moderator,
    )

    assert result["data"]["threadsBulkDelete"] == {
        "deleted": [str(thread.id)],
        "errors": [
            {
                "location": "threads.0",
                "type": "thread_error.not_found",
            },
        ],
    }

    with pytest.raises(Thread.DoesNotExist):
        await thread.fetch_from_db()
