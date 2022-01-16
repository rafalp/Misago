import pytest

from .....errors import ErrorsList

THREAD_TITLE_UPDATE_MUTATION = """
    mutation ThreadTitleUpdate($input: ThreadTitleUpdateInput!) {
        threadTitleUpdate(input: $input) {
            thread {
                id
                title
                slug
            }
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_thread_title_update_mutation_updates_thread(
    query_public_api, user, user_thread
):
    result = await query_public_api(
        THREAD_TITLE_UPDATE_MUTATION,
        {"input": {"thread": str(user_thread.id), "title": "Edited thread"}},
        auth=user,
    )

    assert result["data"]["threadTitleUpdate"] == {
        "thread": {
            "id": str(user_thread.id),
            "title": "Edited thread",
            "slug": "edited-thread",
        },
        "errors": None,
    }

    thread_from_db = await user_thread.refresh_from_db()
    assert thread_from_db.title == "Edited thread"
    assert thread_from_db.slug == "edited-thread"


@pytest.mark.asyncio
async def test_thread_title_update_mutation_fails_if_user_is_not_authorized(
    query_public_api, user_thread
):
    result = await query_public_api(
        THREAD_TITLE_UPDATE_MUTATION,
        {"input": {"thread": str(user_thread.id), "title": "Edited thread"}},
    )

    assert result["data"]["threadTitleUpdate"] == {
        "thread": {
            "id": str(user_thread.id),
            "title": "Thread",
            "slug": "thread",
        },
        "errors": [
            {
                "location": "thread",
                "type": "auth_error.thread.not_author",
            },
            {
                "location": ErrorsList.ROOT_LOCATION,
                "type": "auth_error.not_authorized",
            },
        ],
    }

    thread_from_db = await user_thread.refresh_from_db()
    assert thread_from_db.title == "Thread"
    assert thread_from_db.slug == "thread"


@pytest.mark.asyncio
async def test_thread_title_update_mutation_fails_if_thread_id_is_invalid(
    query_public_api, user
):
    result = await query_public_api(
        THREAD_TITLE_UPDATE_MUTATION,
        {"input": {"thread": "invalid", "title": "Edited thread"}},
        auth=user,
    )

    assert result["data"]["threadTitleUpdate"] == {
        "thread": None,
        "errors": [
            {
                "location": "thread",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_thread_title_update_mutation_fails_if_thread_doesnt_exist(
    query_public_api, user
):
    result = await query_public_api(
        THREAD_TITLE_UPDATE_MUTATION,
        {"input": {"thread": "invalid", "title": "Edited thread"}},
        auth=user,
    )

    assert result["data"]["threadTitleUpdate"] == {
        "thread": None,
        "errors": [
            {
                "location": "thread",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_thread_title_update_mutation_fails_if_thread_author_is_other_user(
    query_public_api, user, other_user_thread
):
    result = await query_public_api(
        THREAD_TITLE_UPDATE_MUTATION,
        {"input": {"thread": str(other_user_thread.id), "title": "Edited thread"}},
        auth=user,
    )

    assert result["data"]["threadTitleUpdate"] == {
        "thread": {
            "id": str(other_user_thread.id),
            "title": "Thread",
            "slug": "thread",
        },
        "errors": [
            {
                "location": "thread",
                "type": "auth_error.thread.not_author",
            },
        ],
    }

    thread_from_db = await other_user_thread.refresh_from_db()
    assert thread_from_db.title == "Thread"
    assert thread_from_db.slug == "thread"


@pytest.mark.asyncio
async def test_thread_title_update_mutation_allows_moderator_to_edit_other_user_thread(
    query_public_api, moderator, other_user_thread
):
    result = await query_public_api(
        THREAD_TITLE_UPDATE_MUTATION,
        {"input": {"thread": str(other_user_thread.id), "title": "Edited thread"}},
        auth=moderator,
    )

    assert result["data"]["threadTitleUpdate"] == {
        "thread": {
            "id": str(other_user_thread.id),
            "title": "Edited thread",
            "slug": "edited-thread",
        },
        "errors": None,
    }

    thread_from_db = await other_user_thread.refresh_from_db()
    assert thread_from_db.title == "Edited thread"
    assert thread_from_db.slug == "edited-thread"


@pytest.mark.asyncio
async def test_thread_title_update_mutation_fails_if_thread_is_closed(
    query_public_api, user, closed_user_thread
):
    result = await query_public_api(
        THREAD_TITLE_UPDATE_MUTATION,
        {"input": {"thread": str(closed_user_thread.id), "title": "Edited thread"}},
        auth=user,
    )

    assert result["data"]["threadTitleUpdate"] == {
        "thread": {
            "id": str(closed_user_thread.id),
            "title": "Thread",
            "slug": "thread",
        },
        "errors": [
            {
                "location": "thread",
                "type": "auth_error.thread.closed",
            },
        ],
    }

    thread_from_db = await closed_user_thread.refresh_from_db()
    assert thread_from_db.title == "Thread"
    assert thread_from_db.slug == "thread"


@pytest.mark.asyncio
async def test_thread_title_update_mutation_allows_moderator_to_title_update_in_closed_thread(
    query_public_api, moderator, closed_user_thread
):
    result = await query_public_api(
        THREAD_TITLE_UPDATE_MUTATION,
        {"input": {"thread": str(closed_user_thread.id), "title": "Edited thread"}},
        auth=moderator,
    )

    assert result["data"]["threadTitleUpdate"] == {
        "thread": {
            "id": str(closed_user_thread.id),
            "title": "Edited thread",
            "slug": "edited-thread",
        },
        "errors": None,
    }

    thread_from_db = await closed_user_thread.refresh_from_db()
    assert thread_from_db.title == "Edited thread"
    assert thread_from_db.slug == "edited-thread"


@pytest.mark.asyncio
async def test_thread_title_update_mutation_fails_if_category_is_closed(
    query_public_api, user, closed_category_user_thread
):
    result = await query_public_api(
        THREAD_TITLE_UPDATE_MUTATION,
        {
            "input": {
                "thread": str(closed_category_user_thread.id),
                "title": "Edited thread",
            }
        },
        auth=user,
    )

    assert result["data"]["threadTitleUpdate"] == {
        "thread": {
            "id": str(closed_category_user_thread.id),
            "title": "Thread",
            "slug": "thread",
        },
        "errors": [
            {
                "location": "thread",
                "type": "auth_error.category.closed",
            },
        ],
    }

    thread_from_db = await closed_category_user_thread.refresh_from_db()
    assert thread_from_db.title == "Thread"
    assert thread_from_db.slug == "thread"


@pytest.mark.asyncio
async def test_thread_title_update_mutation_allows_moderator_to_title_update_in_closed_category(
    query_public_api, moderator, closed_category_user_thread
):
    result = await query_public_api(
        THREAD_TITLE_UPDATE_MUTATION,
        {
            "input": {
                "thread": str(closed_category_user_thread.id),
                "title": "Edited thread",
            }
        },
        auth=moderator,
    )

    assert result["data"]["threadTitleUpdate"] == {
        "thread": {
            "id": str(closed_category_user_thread.id),
            "title": "Edited thread",
            "slug": "edited-thread",
        },
        "errors": None,
    }

    thread_from_db = await closed_category_user_thread.refresh_from_db()
    assert thread_from_db.title == "Edited thread"
    assert thread_from_db.slug == "edited-thread"
