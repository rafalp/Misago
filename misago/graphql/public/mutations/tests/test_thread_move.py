import pytest

from .....errors import ErrorsList

THREAD_MOVE_MUTATION = """
    mutation ThreadMove($thread: ID!, $category: ID!) {
        threadMove(thread: $thread, category: $category) {
            thread {
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
async def test_thread_move_mutation_moves_thread(
    query_public_api, moderator, thread, sibling_category
):
    result = await query_public_api(
        THREAD_MOVE_MUTATION,
        {"thread": str(thread.id), "category": str(sibling_category.id)},
        auth=moderator,
    )

    assert result["data"]["threadMove"] == {
        "thread": {
            "id": str(thread.id),
            "category": {
                "id": str(sibling_category.id),
            },
        },
        "errors": None,
    }

    thread_from_db = await thread.refresh_from_db()
    assert thread_from_db.category_id == sibling_category.id


@pytest.mark.asyncio
async def test_thread_move_mutation_fails_if_user_is_not_authorized(
    query_public_api, thread, sibling_category
):
    result = await query_public_api(
        THREAD_MOVE_MUTATION,
        {"thread": str(thread.id), "category": str(sibling_category.id)},
    )

    assert result["data"]["threadMove"] == {
        "thread": {
            "id": str(thread.id),
            "category": {
                "id": str(thread.category_id),
            },
        },
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

    thread_from_db = await thread.refresh_from_db()
    assert thread_from_db.category_id == thread.category_id


@pytest.mark.asyncio
async def test_thread_move_mutation_fails_if_user_is_not_moderator(
    query_public_api, user, thread, sibling_category
):
    result = await query_public_api(
        THREAD_MOVE_MUTATION,
        {"thread": str(thread.id), "category": str(sibling_category.id)},
        auth=user,
    )

    assert result["data"]["threadMove"] == {
        "thread": {
            "id": str(thread.id),
            "category": {
                "id": str(thread.category_id),
            },
        },
        "errors": [
            {
                "location": "thread",
                "type": "auth_error.not_moderator",
            },
        ],
    }

    thread_from_db = await thread.refresh_from_db()
    assert thread_from_db.category_id == thread.category_id


@pytest.mark.asyncio
async def test_thread_move_mutation_fails_if_thread_id_is_invalid(
    query_public_api, moderator, sibling_category
):
    result = await query_public_api(
        THREAD_MOVE_MUTATION,
        {"thread": "invalid", "category": str(sibling_category.id)},
        auth=moderator,
    )

    assert result["data"]["threadMove"] == {
        "thread": None,
        "errors": [
            {
                "location": "thread",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_thread_move_mutation_fails_if_thread_doesnt_exist(
    query_public_api, moderator, sibling_category
):
    result = await query_public_api(
        THREAD_MOVE_MUTATION,
        {"thread": "4000", "category": str(sibling_category.id)},
        auth=moderator,
    )

    assert result["data"]["threadMove"] == {
        "thread": None,
        "errors": [
            {
                "location": "thread",
                "type": "value_error.thread.not_exists",
            },
        ],
    }


@pytest.mark.asyncio
async def test_thread_move_mutation_fails_if_category_id_is_invalid(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        THREAD_MOVE_MUTATION,
        {"thread": str(thread.id), "category": "invalid"},
        auth=moderator,
    )

    assert result["data"]["threadMove"] == {
        "thread": {
            "id": str(thread.id),
            "category": {
                "id": str(thread.category_id),
            },
        },
        "errors": [
            {
                "location": "category",
                "type": "type_error.integer",
            },
        ],
    }

    thread_from_db = await thread.refresh_from_db()
    assert thread_from_db.category_id == thread.category_id


@pytest.mark.asyncio
async def test_thread_move_mutation_fails_if_category_doesnt_exist(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        THREAD_MOVE_MUTATION,
        {"thread": str(thread.id), "category": "4000"},
        auth=moderator,
    )

    assert result["data"]["threadMove"] == {
        "thread": {
            "id": str(thread.id),
            "category": {
                "id": str(thread.category_id),
            },
        },
        "errors": [
            {
                "location": "category",
                "type": "value_error.category.not_exists",
            },
        ],
    }

    thread_from_db = await thread.refresh_from_db()
    assert thread_from_db.category_id == thread.category_id
