import pytest

from .....errors import ErrorsList

THREADS_BULK_OPEN_MUTATION = """
    mutation ThreadsOpen($threads: [ID!]!) {
        threadsBulkOpen(threads: $threads) {
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
async def test_threads_bulk_open_mutation_opens_threads(
    query_public_api, moderator, closed_thread
):
    result = await query_public_api(
        THREADS_BULK_OPEN_MUTATION,
        {"threads": [str(closed_thread.id)]},
        auth=moderator,
    )

    assert result["data"]["threadsBulkOpen"] == {
        "updated": [str(closed_thread.id)],
        "threads": [
            {
                "id": str(closed_thread.id),
                "isClosed": False,
            },
        ],
        "errors": None,
    }

    thread_from_db = await closed_thread.fetch_from_db()
    assert not thread_from_db.is_closed


@pytest.mark.asyncio
async def test_threads_bulk_open_mutation_skips_open_threads(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        THREADS_BULK_OPEN_MUTATION,
        {"threads": [str(thread.id)]},
        auth=moderator,
    )

    assert result["data"]["threadsBulkOpen"] == {
        "updated": [],
        "threads": [
            {
                "id": str(thread.id),
                "isClosed": False,
            },
        ],
        "errors": None,
    }

    thread_from_db = await thread.fetch_from_db()
    assert not thread_from_db.is_closed


@pytest.mark.asyncio
async def test_threads_bulk_open_mutation_fails_if_user_is_not_authorized(
    query_public_api, closed_thread
):
    result = await query_public_api(
        THREADS_BULK_OPEN_MUTATION,
        {"threads": [str(closed_thread.id)]},
    )

    assert result["data"]["threadsBulkOpen"] == {
        "updated": [],
        "threads": [
            {
                "id": str(closed_thread.id),
                "isClosed": True,
            },
        ],
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

    thread_from_db = await closed_thread.fetch_from_db()
    assert thread_from_db.is_closed


@pytest.mark.asyncio
async def test_threads_bulk_open_mutation_fails_if_user_is_not_moderator(
    query_public_api, user, closed_thread
):
    result = await query_public_api(
        THREADS_BULK_OPEN_MUTATION,
        {"threads": [str(closed_thread.id)]},
        auth=user,
    )

    assert result["data"]["threadsBulkOpen"] == {
        "updated": [],
        "threads": [
            {
                "id": str(closed_thread.id),
                "isClosed": True,
            },
        ],
        "errors": [
            {
                "location": "threads.0",
                "type": "auth_error.not_moderator",
            },
        ],
    }

    thread_from_db = await closed_thread.fetch_from_db()
    assert thread_from_db.is_closed


@pytest.mark.asyncio
async def test_threads_bulk_open_mutation_fails_if_thread_id_is_invalid(
    query_public_api, moderator
):
    result = await query_public_api(
        THREADS_BULK_OPEN_MUTATION,
        {"threads": ["invalid"]},
        auth=moderator,
    )

    assert result["data"]["threadsBulkOpen"] == {
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
async def test_threads_bulk_open_mutation_fails_if_thread_doesnt_exist(
    query_public_api, moderator
):
    result = await query_public_api(
        THREADS_BULK_OPEN_MUTATION,
        {"threads": ["4000"]},
        auth=moderator,
    )

    assert result["data"]["threadsBulkOpen"] == {
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
async def test_threads_bulk_open_mutation_with_threads_errors_still_updates_valid_threads(
    query_public_api, moderator, closed_thread
):
    result = await query_public_api(
        THREADS_BULK_OPEN_MUTATION,
        {"threads": ["4000", str(closed_thread.id)]},
        auth=moderator,
    )

    assert result["data"]["threadsBulkOpen"] == {
        "updated": [str(closed_thread.id)],
        "threads": [
            {
                "id": str(closed_thread.id),
                "isClosed": False,
            },
        ],
        "errors": [
            {
                "location": "threads.0",
                "type": "value_error.thread.not_found",
            },
        ],
    }

    thread_from_db = await closed_thread.fetch_from_db()
    assert not thread_from_db.is_closed
