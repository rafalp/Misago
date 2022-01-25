import pytest

from .....errors import ErrorsList

THREADS_BULK_CLOSE_MUTATION = """
    mutation ThreadsClose($threads: [ID!]!) {
        threadsBulkClose(threads: $threads) {
            updated
            threads {
                id
                isClosed
            }
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_threads_bulk_close_mutation_closes_threads(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        THREADS_BULK_CLOSE_MUTATION,
        {"threads": [str(thread.id)]},
        auth=moderator,
    )

    assert result["data"]["threadsBulkClose"] == {
        "updated": [str(thread.id)],
        "threads": [
            {
                "id": str(thread.id),
                "isClosed": True,
            },
        ],
        "errors": None,
    }

    thread_from_db = await thread.fetch_from_db()
    assert thread_from_db.is_closed


@pytest.mark.asyncio
async def test_threads_bulk_close_mutation_skips_closed_threads(
    query_public_api, moderator, closed_thread
):
    result = await query_public_api(
        THREADS_BULK_CLOSE_MUTATION,
        {"threads": [str(closed_thread.id)]},
        auth=moderator,
    )

    assert result["data"]["threadsBulkClose"] == {
        "updated": [],
        "threads": [
            {
                "id": str(closed_thread.id),
                "isClosed": True,
            },
        ],
        "errors": None,
    }

    thread_from_db = await closed_thread.fetch_from_db()
    assert thread_from_db.is_closed


@pytest.mark.asyncio
async def test_threads_bulk_close_mutation_fails_if_user_is_not_authenticated(
    query_public_api, thread
):
    result = await query_public_api(
        THREADS_BULK_CLOSE_MUTATION,
        {"threads": [str(thread.id)]},
    )

    assert result["data"]["threadsBulkClose"] == {
        "updated": [],
        "threads": [
            {
                "id": str(thread.id),
                "isClosed": False,
            },
        ],
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

    thread_from_db = await thread.fetch_from_db()
    assert not thread_from_db.is_closed


@pytest.mark.asyncio
async def test_threads_bulk_close_mutation_fails_if_user_is_not_moderator(
    query_public_api, user, thread
):
    result = await query_public_api(
        THREADS_BULK_CLOSE_MUTATION,
        {"threads": [str(thread.id)]},
        auth=user,
    )

    assert result["data"]["threadsBulkClose"] == {
        "updated": [],
        "threads": [
            {
                "id": str(thread.id),
                "isClosed": False,
            },
        ],
        "errors": [
            {
                "location": "threads.0",
                "type": "auth_error.not_moderator",
            },
        ],
    }

    thread_from_db = await thread.fetch_from_db()
    assert not thread_from_db.is_closed


@pytest.mark.asyncio
async def test_threads_bulk_close_mutation_fails_if_thread_id_is_invalid(
    query_public_api, moderator
):
    result = await query_public_api(
        THREADS_BULK_CLOSE_MUTATION,
        {"threads": ["invalid"]},
        auth=moderator,
    )

    assert result["data"]["threadsBulkClose"] == {
        "updated": [],
        "threads": [],
        "errors": [
            {
                "location": "threads.0",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_threads_bulk_close_mutation_fails_if_thread_doesnt_exist(
    query_public_api, moderator
):
    result = await query_public_api(
        THREADS_BULK_CLOSE_MUTATION,
        {"threads": ["4000"]},
        auth=moderator,
    )

    assert result["data"]["threadsBulkClose"] == {
        "updated": [],
        "threads": [],
        "errors": [
            {
                "location": "threads.0",
                "type": "value_error.thread.not_found",
            },
        ],
    }


@pytest.mark.asyncio
async def test_threads_bulk_close_mutation_with_threads_errors_still_updates_valid_threads(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        THREADS_BULK_CLOSE_MUTATION,
        {"threads": ["4000", str(thread.id)]},
        auth=moderator,
    )

    assert result["data"]["threadsBulkClose"] == {
        "updated": [str(thread.id)],
        "threads": [
            {
                "id": str(thread.id),
                "isClosed": True,
            },
        ],
        "errors": [
            {
                "location": "threads.0",
                "type": "value_error.thread.not_found",
            },
        ],
    }

    thread_from_db = await thread.fetch_from_db()
    assert thread_from_db.is_closed
