from unittest.mock import ANY

import pytest

from .....errors import ErrorsList
from .....pubsub.threads import THREADS_CHANNEL
from .....threads.models import Post

POST_CREATE_MUTATION = """
    mutation PostCreate($input: PostCreateInput!) {
        postCreate(input: $input) {
            thread {
                id
            }
            post {
                id
                richText
            }
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_post_create_mutation_creates_new_reply(
    broadcast_publish, query_public_api, user, thread
):
    result = await query_public_api(
        POST_CREATE_MUTATION,
        {"input": {"thread": str(thread.id), "markup": "This is test post!"}},
        auth=user,
    )

    data = result["data"]["postCreate"]

    assert data == {
        "thread": {
            "id": str(thread.id),
        },
        "post": {
            "id": ANY,
            "richText": [
                {"id": ANY, "type": "p", "text": "This is test post!"},
            ],
        },
        "errors": None,
    }

    thread_from_db = await thread.refresh_from_db()
    post_from_db = await Post.query.one(id=int(data["post"]["id"]))

    assert thread_from_db.started_at == thread.started_at
    assert thread_from_db.last_posted_at > thread.last_posted_at
    assert thread_from_db.last_posted_at == post_from_db.posted_at
    assert thread_from_db.last_poster_id == user.id
    assert thread_from_db.last_poster_name == user.name
    assert thread_from_db.last_post_id == post_from_db.id
    assert thread_from_db.replies == thread.replies + 1

    assert post_from_db.thread_id == thread.id
    assert post_from_db.category_id == thread.category_id
    assert post_from_db.poster_id == user.id
    assert post_from_db.poster_name == user.name
    assert post_from_db.markup == "This is test post!"
    assert post_from_db.rich_text[0]["type"] == "p"
    assert post_from_db.rich_text[0]["text"] == "This is test post!"

    # Thread update sent to subscribers
    broadcast_publish.assert_called_once_with(channel=THREADS_CHANNEL, message=ANY)


@pytest.mark.asyncio
async def test_post_create_mutation_fails_if_user_is_not_authorized(
    query_public_api, thread
):
    result = await query_public_api(
        POST_CREATE_MUTATION,
        {"input": {"thread": str(thread.id), "markup": "This is test post!"}},
    )

    assert result["data"]["postCreate"] == {
        "thread": {
            "id": str(thread.id),
        },
        "post": None,
        "errors": [
            {
                "location": ErrorsList.ROOT_LOCATION,
                "type": "auth_error.not_authorized",
            }
        ],
    }


@pytest.mark.asyncio
async def test_post_create_mutation_fails_if_thread_id_is_invalid(
    query_public_api, user
):
    result = await query_public_api(
        POST_CREATE_MUTATION,
        {"input": {"thread": "invalid", "markup": "This is test post!"}},
        auth=user,
    )

    assert result["data"]["postCreate"] == {
        "thread": None,
        "post": None,
        "errors": [
            {
                "location": "thread",
                "type": "type_error.integer",
            }
        ],
    }


@pytest.mark.asyncio
async def test_post_create_mutation_fails_if_thread_doesnt_exist(query_public_api, user):
    result = await query_public_api(
        POST_CREATE_MUTATION,
        {"input": {"thread": "4000", "markup": "This is test post!"}},
        auth=user,
    )

    assert result["data"]["postCreate"] == {
        "thread": None,
        "post": None,
        "errors": [
            {
                "location": "thread",
                "type": "value_error.thread.not_exists",
            }
        ],
    }


@pytest.mark.asyncio
async def test_post_create_mutation_fails_if_thread_is_closed(
    query_public_api, user, closed_thread
):
    result = await query_public_api(
        POST_CREATE_MUTATION,
        {"input": {"thread": str(closed_thread.id), "markup": "This is test post!"}},
        auth=user,
    )

    assert result["data"]["postCreate"] == {
        "thread": {
            "id": str(closed_thread.id),
        },
        "post": None,
        "errors": [
            {
                "location": "thread",
                "type": "auth_error.thread.closed",
            }
        ],
    }


@pytest.mark.asyncio
async def test_post_create_mutation_allows_moderator_to_post_create_in_closed_thread(
    broadcast_publish, query_public_api, moderator, closed_thread
):
    result = await query_public_api(
        POST_CREATE_MUTATION,
        {"input": {"thread": str(closed_thread.id), "markup": "This is test post!"}},
        auth=moderator,
    )

    assert result["data"]["postCreate"] == {
        "thread": {
            "id": str(closed_thread.id),
        },
        "post": {
            "id": ANY,
            "richText": [
                {"id": ANY, "type": "p", "text": "This is test post!"},
            ],
        },
        "errors": None,
    }

    broadcast_publish.assert_called_once()


@pytest.mark.asyncio
async def test_post_create_mutation_fails_if_category_is_closed(
    query_public_api, user, closed_category_thread
):
    result = await query_public_api(
        POST_CREATE_MUTATION,
        {
            "input": {
                "thread": str(closed_category_thread.id),
                "markup": "This is test post!",
            }
        },
        auth=user,
    )

    assert result["data"]["postCreate"] == {
        "thread": {
            "id": str(closed_category_thread.id),
        },
        "post": None,
        "errors": [
            {
                "location": "thread",
                "type": "auth_error.category.closed",
            },
        ],
    }


@pytest.mark.asyncio
async def test_post_create_mutation_allows_moderator_to_post_create_in_closed_category(
    broadcast_publish, query_public_api, moderator, closed_category_thread
):
    result = await query_public_api(
        POST_CREATE_MUTATION,
        {
            "input": {
                "thread": str(closed_category_thread.id),
                "markup": "This is test post!",
            }
        },
        auth=moderator,
    )

    assert result["data"]["postCreate"] == {
        "thread": {
            "id": str(closed_category_thread.id),
        },
        "post": {
            "id": ANY,
            "richText": [
                {"id": ANY, "type": "p", "text": "This is test post!"},
            ],
        },
        "errors": None,
    }

    broadcast_publish.assert_called_once()


@pytest.mark.asyncio
async def test_post_create_mutation_fails_if_markup_is_too_short(
    query_public_api, user, thread
):
    result = await query_public_api(
        POST_CREATE_MUTATION,
        {"input": {"thread": str(thread.id), "markup": " "}},
        auth=user,
    )

    assert result["data"]["postCreate"] == {
        "thread": {
            "id": str(thread.id),
        },
        "post": None,
        "errors": [
            {
                "location": "markup",
                "type": "value_error.any_str.min_length",
            }
        ],
    }
