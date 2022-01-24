import pytest

from .....errors import ErrorsList

THREADS_BULK_MOVE_MUTATION = """
    mutation ThreadsBulkMove($threads: [ID!]!, $category: ID!) {
        threadsBulkMove(threads: $threads, category: $category) {
            updated
            threads {
                id
                category {
                    id
                }
            }
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_threads_bulk_move_mutation_moves_threads(
    query_public_api, moderator, thread, sibling_category
):
    result = await query_public_api(
        THREADS_BULK_MOVE_MUTATION,
        {"threads": [str(thread.id)], "category": str(sibling_category.id)},
        auth=moderator,
    )

    assert result["data"]["threadsBulkMove"] == {
        "updated": [str(thread.id)],
        "threads": [
            {
                "id": str(thread.id),
                "category": {
                    "id": str(sibling_category.id),
                },
            },
        ],
        "errors": None,
    }

    thread_from_db = await thread.fetch_from_db()
    assert thread_from_db.category_id == sibling_category.id


@pytest.mark.asyncio
async def test_threads_bulk_move_doesnt_move_threads_in_target_category(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        THREADS_BULK_MOVE_MUTATION,
        {"threads": [str(thread.id)], "category": str(thread.category_id)},
        auth=moderator,
    )

    assert result["data"]["threadsBulkMove"] == {
        "updated": [],
        "threads": [
            {
                "id": str(thread.id),
                "category": {
                    "id": str(thread.category_id),
                },
            },
        ],
        "errors": None,
    }

    thread_from_db = await thread.fetch_from_db()
    assert thread_from_db.category_id == thread.category_id


@pytest.mark.asyncio
async def test_threads_bulk_move_mutation_fails_if_user_is_not_authorized(
    query_public_api, thread, sibling_category
):
    result = await query_public_api(
        THREADS_BULK_MOVE_MUTATION,
        {"threads": [str(thread.id)], "category": str(sibling_category.id)},
    )

    assert result["data"]["threadsBulkMove"] == {
        "updated": [],
        "threads": [
            {
                "id": str(thread.id),
                "category": {
                    "id": str(thread.category_id),
                },
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

    thread_from_db = await thread.fetch_from_db()
    assert thread_from_db.category_id == thread.category_id


@pytest.mark.asyncio
async def test_threads_bulk_move_mutation_fails_if_user_is_not_moderator(
    query_public_api, user, thread, sibling_category
):
    result = await query_public_api(
        THREADS_BULK_MOVE_MUTATION,
        {"threads": [str(thread.id)], "category": str(sibling_category.id)},
        auth=user,
    )

    assert result["data"]["threadsBulkMove"] == {
        "updated": [],
        "threads": [
            {
                "id": str(thread.id),
                "category": {
                    "id": str(thread.category_id),
                },
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
    assert thread_from_db.category_id == thread.category_id


@pytest.mark.asyncio
async def test_threads_bulk_move_mutation_fails_if_thread_id_is_invalid(
    query_public_api, moderator, sibling_category
):
    result = await query_public_api(
        THREADS_BULK_MOVE_MUTATION,
        {"threads": ["invalid"], "category": str(sibling_category.id)},
        auth=moderator,
    )

    assert result["data"]["threadsBulkMove"] == {
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
async def test_threads_bulk_move_mutation_fails_if_thread_doesnt_exist(
    query_public_api, moderator, sibling_category
):
    result = await query_public_api(
        THREADS_BULK_MOVE_MUTATION,
        {"threads": ["4000"], "category": str(sibling_category.id)},
        auth=moderator,
    )

    assert result["data"]["threadsBulkMove"] == {
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
async def test_threads_bulk_move_mutation_fails_if_category_id_is_invalid(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        THREADS_BULK_MOVE_MUTATION,
        {"threads": [str(thread.id)], "category": "invalid"},
        auth=moderator,
    )

    assert result["data"]["threadsBulkMove"] == {
        "updated": [],
        "threads": [
            {
                "id": str(thread.id),
                "category": {
                    "id": str(thread.category_id),
                },
            },
        ],
        "errors": [
            {
                "location": "category",
                "type": "type_error.integer",
            },
        ],
    }

    thread_from_db = await thread.fetch_from_db()
    assert thread_from_db.category_id == thread.category_id


@pytest.mark.asyncio
async def test_threads_bulk_move_mutation_fails_if_category_doesnt_exist(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        THREADS_BULK_MOVE_MUTATION,
        {"threads": [str(thread.id)], "category": "1000"},
        auth=moderator,
    )

    assert result["data"]["threadsBulkMove"] == {
        "updated": [],
        "threads": [
            {
                "id": str(thread.id),
                "category": {
                    "id": str(thread.category_id),
                },
            },
        ],
        "errors": [
            {
                "location": "category",
                "type": "value_error.category.not_found",
            },
        ],
    }

    thread_from_db = await thread.fetch_from_db()
    assert thread_from_db.category_id == thread.category_id


@pytest.mark.asyncio
async def test_threads_bulk_move_mutation_with_threads_errors_still_updates_valid_threads(
    query_public_api, moderator, thread, sibling_category
):
    result = await query_public_api(
        THREADS_BULK_MOVE_MUTATION,
        {
            "threads": ["4000", str(thread.id)],
            "category": str(sibling_category.id),
        },
        auth=moderator,
    )

    assert result["data"]["threadsBulkMove"] == {
        "updated": [str(thread.id)],
        "threads": [
            {
                "id": str(thread.id),
                "category": {
                    "id": str(sibling_category.id),
                },
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
    assert thread_from_db.category_id == sibling_category.id
