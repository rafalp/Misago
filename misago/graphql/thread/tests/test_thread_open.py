import pytest

from ....validation import ROOT_LOCATION

THREAD_OPEN_MUTATION = """
    mutation ThreadOpen($thread: ID!) {
        threadOpen(thread: $thread) {
            updated
            thread {
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
async def test_thread_open_mutation_opens_thread(
    query_public_api, moderator, closed_thread
):
    result = await query_public_api(
        THREAD_OPEN_MUTATION,
        {"thread": str(closed_thread.id)},
        auth=moderator,
    )

    assert result["data"]["threadOpen"] == {
        "updated": True,
        "thread": {
            "id": str(closed_thread.id),
            "isClosed": False,
        },
        "errors": None,
    }

    thread_from_db = await closed_thread.fetch_from_db()
    assert not thread_from_db.is_closed


@pytest.mark.asyncio
async def test_thread_open_mutation_does_nothing_for_open_thread(
    query_public_api, moderator, thread
):
    result = await query_public_api(
        THREAD_OPEN_MUTATION,
        {"thread": str(thread.id)},
        auth=moderator,
    )

    assert result["data"]["threadOpen"] == {
        "updated": False,
        "thread": {
            "id": str(thread.id),
            "isClosed": False,
        },
        "errors": None,
    }

    thread_from_db = await thread.fetch_from_db()
    assert not thread_from_db.is_closed


@pytest.mark.asyncio
async def test_thread_open_mutation_fails_if_user_is_not_authenticated(
    query_public_api, closed_thread
):
    result = await query_public_api(
        THREAD_OPEN_MUTATION,
        {"thread": str(closed_thread.id)},
    )

    assert result["data"]["threadOpen"] == {
        "updated": False,
        "thread": {
            "id": str(closed_thread.id),
            "isClosed": True,
        },
        "errors": [
            {
                "location": "thread",
                "type": "auth_error.not_moderator",
            },
            {
                "location": ROOT_LOCATION,
                "type": "auth_error.not_authenticated",
            },
        ],
    }

    thread_from_db = await closed_thread.fetch_from_db()
    assert thread_from_db.is_closed


@pytest.mark.asyncio
async def test_thread_open_mutation_fails_if_user_is_not_moderator(
    query_public_api, user, closed_thread
):
    result = await query_public_api(
        THREAD_OPEN_MUTATION,
        {"thread": str(closed_thread.id)},
        auth=user,
    )

    assert result["data"]["threadOpen"] == {
        "updated": False,
        "thread": {
            "id": str(closed_thread.id),
            "isClosed": True,
        },
        "errors": [
            {
                "location": "thread",
                "type": "auth_error.not_moderator",
            },
        ],
    }

    thread_from_db = await closed_thread.fetch_from_db()
    assert thread_from_db.is_closed


@pytest.mark.asyncio
async def test_thread_open_mutation_fails_if_thread_id_is_invalid(
    query_public_api, moderator
):
    result = await query_public_api(
        THREAD_OPEN_MUTATION,
        {"thread": "invalid"},
        auth=moderator,
    )

    assert result["data"]["threadOpen"] == {
        "updated": False,
        "thread": None,
        "errors": [
            {
                "location": "thread",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_thread_open_mutation_fails_if_thread_doesnt_exist(
    query_public_api, moderator
):
    result = await query_public_api(
        THREAD_OPEN_MUTATION,
        {"thread": "4000"},
        auth=moderator,
    )

    assert result["data"]["threadOpen"] == {
        "updated": False,
        "thread": None,
        "errors": [
            {
                "location": "thread",
                "type": "thread_error.not_found",
            },
        ],
    }
