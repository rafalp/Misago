from os import close
from unittest.mock import ANY

import pytest

from .....errors import ErrorsList
from .....pubsub.threads import THREADS_CHANNEL
from .....testing import override_dynamic_settings
from .....threads.models import Post, Thread

POST_THREAD_MUTATION = """
    mutation PostThread($input: PostThreadInput!) {
        postThread(input: $input) {
            thread {
                id
                category {
                    id
                }
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
async def test_post_thread_mutation_creates_new_thread(
    publish, query_public_api, user, category
):
    result = await query_public_api(
        POST_THREAD_MUTATION,
        {
            "input": {
                "category": str(category.id),
                "title": "Hello world!",
                "markup": "This is test post!",
            },
        },
        auth=user,
    )

    data = result["data"]["postThread"]

    assert data == {
        "thread": {
            "id": ANY,
            "category": {"id": str(category.id)},
            "isClosed": False,
        },
        "errors": None,
    }

    thread_from_db = await Thread.query.one(id=int(data["thread"]["id"]))
    post_from_db = await Post.query.one(id=thread_from_db.first_post_id)

    assert thread_from_db.category_id == category.id
    assert thread_from_db.started_at == post_from_db.posted_at
    assert thread_from_db.starter_id == user.id
    assert thread_from_db.starter_name == user.name
    assert thread_from_db.first_post_id == post_from_db.id
    assert thread_from_db.last_posted_at == post_from_db.posted_at
    assert thread_from_db.last_poster_id == user.id
    assert thread_from_db.last_poster_name == user.name
    assert thread_from_db.last_post_id == post_from_db.id
    assert thread_from_db.replies == 0
    assert not thread_from_db.is_closed

    assert post_from_db.thread_id == thread_from_db.id
    assert post_from_db.category_id == category.id
    assert post_from_db.poster_id == user.id
    assert post_from_db.poster_name == user.name
    assert post_from_db.markup == "This is test post!"
    assert post_from_db.rich_text[0]["type"] == "p"
    assert post_from_db.rich_text[0]["text"] == "This is test post!"

    # Thread sent to subscribers
    publish.assert_called_once_with(channel=THREADS_CHANNEL, message=ANY)


@pytest.mark.asyncio
async def test_post_thread_mutation_fails_if_user_is_not_authorized(
    query_public_api, category
):
    result = await query_public_api(
        POST_THREAD_MUTATION,
        {
            "input": {
                "category": str(category.id),
                "title": "Hello world!",
                "markup": "This is test post!",
            },
        },
    )

    assert result["data"]["postThread"] == {
        "thread": None,
        "errors": [
            {
                "location": [ErrorsList.ROOT_LOCATION],
                "type": "auth_error.not_authorized",
            },
        ],
    }


@pytest.mark.asyncio
async def test_post_thread_mutation_fails_if_category_id_is_invalid(
    query_public_api, user
):
    result = await query_public_api(
        POST_THREAD_MUTATION,
        {
            "input": {
                "category": "invalid",
                "title": "Hello world!",
                "markup": "This is test post!",
            },
        },
        auth=user,
    )

    assert result["data"]["postThread"] == {
        "thread": None,
        "errors": [
            {
                "location": ["category"],
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_post_thread_mutation_fails_if_category_doesnt_exist(
    query_public_api, user
):
    result = await query_public_api(
        POST_THREAD_MUTATION,
        {
            "input": {
                "category": "4000",
                "title": "Hello world!",
                "markup": "This is test post!",
            },
        },
        auth=user,
    )

    assert result["data"]["postThread"] == {
        "thread": None,
        "errors": [
            {
                "location": ["category"],
                "type": "value_error.category.not_exists",
            },
        ],
    }


@pytest.mark.asyncio
@override_dynamic_settings(thread_title_min_length=5)
async def test_post_thread_mutation_validates_min_title_length(
    query_public_api, user, category
):
    result = await query_public_api(
        POST_THREAD_MUTATION,
        {
            "input": {
                "category": str(category.id),
                "title": "Test",
                "markup": "This is test post!",
            },
        },
        auth=user,
    )

    assert result["data"]["postThread"] == {
        "thread": None,
        "errors": [
            {
                "location": ["title"],
                "type": "value_error.any_str.min_length",
            },
        ],
    }


@pytest.mark.asyncio
@override_dynamic_settings(thread_title_max_length=10)
async def test_post_thread_mutation_validates_max_title_length(
    query_public_api, user, category
):
    result = await query_public_api(
        POST_THREAD_MUTATION,
        {
            "input": {
                "category": str(category.id),
                "title": "Test" * 10,
                "markup": "This is test post!",
            },
        },
        auth=user,
    )

    assert result["data"]["postThread"] == {
        "thread": None,
        "errors": [
            {
                "location": ["title"],
                "type": "value_error.any_str.max_length",
            },
        ],
    }


@pytest.mark.asyncio
async def test_post_thread_mutation_validates_title_contains_alphanumeric_characters(
    query_public_api, user, category
):
    result = await query_public_api(
        POST_THREAD_MUTATION,
        {
            "input": {
                "category": str(category.id),
                "title": "!!!" * 10,
                "markup": "This is test post!",
            },
        },
        auth=user,
    )

    assert result["data"]["postThread"] == {
        "thread": None,
        "errors": [
            {
                "location": ["title"],
                "type": "value_error.str.regex",
            },
        ],
    }


@pytest.mark.asyncio
async def test_post_thread_mutation_fails_if_category_is_closed(
    query_public_api, user, closed_category
):
    result = await query_public_api(
        POST_THREAD_MUTATION,
        {
            "input": {
                "category": str(closed_category.id),
                "title": "Hello world!",
                "markup": "This is test post!",
            },
        },
        auth=user,
    )

    assert result["data"]["postThread"] == {
        "thread": None,
        "errors": [
            {
                "location": ["category"],
                "type": "auth_error.category.closed",
            },
        ],
    }


@pytest.mark.asyncio
async def test_post_thread_mutation_allows_moderator_to_post_thread_in_closed_category(
    publish, query_public_api, moderator, closed_category
):
    result = await query_public_api(
        POST_THREAD_MUTATION,
        {
            "input": {
                "category": str(closed_category.id),
                "title": "Hello world!",
                "markup": "This is test post!",
            },
        },
        auth=moderator,
    )

    assert result["data"]["postThread"] == {
        "thread": {
            "id": ANY,
            "category": {
                "id": str(closed_category.id),
            },
            "isClosed": False,
        },
        "errors": None,
    }

    publish.assert_called_once()


@pytest.mark.asyncio
async def test_post_thread_mutation_creates_open_thread(
    publish, query_public_api, user, category
):
    result = await query_public_api(
        POST_THREAD_MUTATION,
        {
            "input": {
                "category": str(category.id),
                "title": "Hello world!",
                "markup": "This is test post!",
                "isClosed": False,
            },
        },
        auth=user,
    )

    assert result["data"]["postThread"] == {
        "thread": {
            "id": ANY,
            "category": {
                "id": str(category.id),
            },
            "isClosed": False,
        },
        "errors": None,
    }

    publish.assert_called_once()


@pytest.mark.asyncio
async def test_post_thread_mutation_allows_moderator_to_post_closed_thread(
    publish, query_public_api, moderator, category
):
    result = await query_public_api(
        POST_THREAD_MUTATION,
        {
            "input": {
                "category": str(category.id),
                "title": "Hello world!",
                "markup": "This is test post!",
                "isClosed": True,
            },
        },
        auth=moderator,
    )

    assert result["data"]["postThread"] == {
        "thread": {
            "id": ANY,
            "category": {
                "id": str(category.id),
            },
            "isClosed": True,
        },
        "errors": None,
    }

    publish.assert_called_once()


@pytest.mark.asyncio
async def test_post_thread_mutation_fails_if_non_moderator_posts_closed_thread(
    query_public_api, user, category
):
    result = await query_public_api(
        POST_THREAD_MUTATION,
        {
            "input": {
                "category": str(category.id),
                "title": "Hello world!",
                "markup": "This is test post!",
                "isClosed": True,
            },
        },
        auth=user,
    )

    assert result["data"]["postThread"] == {
        "thread": None,
        "errors": [
            {
                "location": ["isClosed"],
                "type": "auth_error.not_moderator",
            },
        ],
    }


@pytest.mark.asyncio
async def test_post_thread_mutation_fails_if_markup_is_too_short(
    query_public_api, user, category
):
    result = await query_public_api(
        POST_THREAD_MUTATION,
        {
            "input": {
                "category": str(category.id),
                "title": "Hello world!",
                "markup": "a",
            },
        },
        auth=user,
    )

    assert result["data"]["postThread"] == {
        "thread": None,
        "errors": [
            {
                "location": ["markup"],
                "type": "value_error.any_str.min_length",
            },
        ],
    }
