import pytest

from .....errors import ErrorsList


THREADS_IS_CLOSED_BULK_MUTATION = """
    mutation ThreadsClose($input: ThreadsIsClosedBulkUpdateInput!) {
        threadsIsClosedBulkUpdate(input: $input) {
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
async def test_threads_is_closed_bulk_mutation_closes_threads(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        THREADS_IS_CLOSED_BULK_MUTATION,
        {"input": {"threads": [str(thread.id)], "isClosed": True}},
        auth=moderator,
    )

    assert result["data"]["threadsIsClosedBulkUpdate"] == {
        "updated": True,
        "threads": [
            {
                "id": str(thread.id),
                "isClosed": True,
            },
        ],
        "errors": None,
    }

    thread_from_db = await thread.refresh_from_db()
    assert thread_from_db.is_closed


@pytest.mark.asyncio
async def test_threads_is_closed_bulk_mutation_opens_threads(
    query_public_api, moderator, closed_thread
):
    result = await query_public_api(
        THREADS_IS_CLOSED_BULK_MUTATION,
        {"input": {"threads": [str(closed_thread.id)], "isClosed": False}},
        auth=moderator,
    )

    assert result["data"]["threadsIsClosedBulkUpdate"] == {
        "updated": True,
        "threads": [
            {
                "id": str(closed_thread.id),
                "isClosed": False,
            },
        ],
        "errors": None,
    }

    thread_from_db = await closed_thread.refresh_from_db()
    assert not thread_from_db.is_closed


@pytest.mark.asyncio
async def test_threads_is_closed_bulk_mutation_fails_if_user_is_not_authorized(
    query_public_api, thread
):
    result = await query_public_api(
        THREADS_IS_CLOSED_BULK_MUTATION,
        {"input": {"threads": [str(thread.id)], "isClosed": True}},
    )

    assert result["data"]["threadsIsClosedBulkUpdate"] == {
        "updated": False,
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
                "type": "auth_error.not_authorized",
            },
        ],
    }

    thread_from_db = await thread.refresh_from_db()
    assert not thread_from_db.is_closed


@pytest.mark.asyncio
async def test_threads_is_closed_bulk_mutation_fails_if_user_is_not_moderator(
    query_public_api, user, thread
):
    result = await query_public_api(
        THREADS_IS_CLOSED_BULK_MUTATION,
        {"input": {"threads": [str(thread.id)], "isClosed": True}},
        auth=user,
    )

    assert result["data"]["threadsIsClosedBulkUpdate"] == {
        "updated": False,
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

    thread_from_db = await thread.refresh_from_db()
    assert not thread_from_db.is_closed


@pytest.mark.asyncio
async def test_threads_is_closed_bulk_mutation_fails_if_thread_id_is_invalid(
    query_public_api, moderator
):
    result = await query_public_api(
        THREADS_IS_CLOSED_BULK_MUTATION,
        {"input": {"threads": ["invalid"], "isClosed": True}},
        auth=moderator,
    )

    assert result["data"]["threadsIsClosedBulkUpdate"] == {
        "updated": False,
        "threads": [],
        "errors": [
            {
                "location": "threads.0",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_threads_is_closed_bulk_mutation_fails_if_thread_doesnt_exist(
    query_public_api, moderator
):
    result = await query_public_api(
        THREADS_IS_CLOSED_BULK_MUTATION,
        {"input": {"threads": ["4000"], "isClosed": True}},
        auth=moderator,
    )

    assert result["data"]["threadsIsClosedBulkUpdate"] == {
        "updated": False,
        "threads": [],
        "errors": [
            {
                "location": "threads.0",
                "type": "value_error.thread.not_exists",
            },
        ],
    }


@pytest.mark.asyncio
async def test_threads_is_closed_bulk_mutation_with_threads_errors_still_updates_valid_threads(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        THREADS_IS_CLOSED_BULK_MUTATION,
        {"input": {"threads": ["4000", str(thread.id)], "isClosed": True}},
        auth=moderator,
    )

    assert result["data"]["threadsIsClosedBulkUpdate"] == {
        "updated": True,
        "threads": [
            {
                "id": str(thread.id),
                "isClosed": True,
            },
        ],
        "errors": [
            {
                "location": "threads.0",
                "type": "value_error.thread.not_exists",
            },
        ],
    }

    thread_from_db = await thread.refresh_from_db()
    assert thread_from_db.is_closed
