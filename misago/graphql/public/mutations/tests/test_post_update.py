from unittest.mock import ANY

import pytest

from .....errors import ErrorsList

POST_UPDATE_MUTATION = """
    mutation PostUpdate($input: PostUpdateInput!) {
        postUpdate(input: $input) {
            updated
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
async def test_post_update_mutation_updates_post(query_public_api, user, user_post):
    result = await query_public_api(
        POST_UPDATE_MUTATION,
        {"input": {"post": str(user_post.id), "markup": "Edited post"}},
        auth=user,
    )

    assert result["data"]["postUpdate"] == {
        "updated": True,
        "thread": {
            "id": str(user_post.thread_id),
        },
        "post": {
            "id": str(user_post.id),
            "richText": [
                {
                    "id": ANY,
                    "type": "p",
                    "text": "Edited post",
                },
            ],
        },
        "errors": None,
    }

    post_from_db = await user_post.fetch_from_db()
    assert post_from_db.rich_text == [
        {
            "id": ANY,
            "type": "p",
            "text": "Edited post",
        }
    ]


@pytest.mark.asyncio
async def test_post_update_mutation_fails_if_user_is_not_authorized(
    query_public_api, user_post
):
    result = await query_public_api(
        POST_UPDATE_MUTATION,
        {"input": {"post": str(user_post.id), "markup": "Edited post"}},
    )

    assert result["data"]["postUpdate"] == {
        "updated": False,
        "thread": {
            "id": str(user_post.thread_id),
        },
        "post": {
            "id": str(user_post.id),
            "richText": [],
        },
        "errors": [
            {
                "location": "post",
                "type": "auth_error.post.not_author",
            },
            {
                "location": ErrorsList.ROOT_LOCATION,
                "type": "auth_error.not_authorized",
            },
        ],
    }

    post_from_db = await user_post.fetch_from_db()
    assert post_from_db.rich_text == []


@pytest.mark.asyncio
async def test_post_update_mutation_fails_if_post_id_is_invalid(query_public_api, user):
    result = await query_public_api(
        POST_UPDATE_MUTATION,
        {"input": {"post": "invalid", "markup": "Edited post"}},
        auth=user,
    )

    assert result["data"]["postUpdate"] == {
        "updated": False,
        "thread": None,
        "post": None,
        "errors": [
            {
                "location": "post",
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_post_update_mutation_fails_if_post_doesnt_exist(query_public_api, user):
    result = await query_public_api(
        POST_UPDATE_MUTATION,
        {"input": {"post": "4000", "markup": "Edited post"}},
        auth=user,
    )

    assert result["data"]["postUpdate"] == {
        "updated": False,
        "thread": None,
        "post": None,
        "errors": [
            {
                "location": "post",
                "type": "value_error.post.not_found",
            },
        ],
    }


@pytest.mark.asyncio
async def test_post_update_mutation_fails_if_post_author_is_other_user(
    query_public_api, user, other_user_post
):
    result = await query_public_api(
        POST_UPDATE_MUTATION,
        {"input": {"post": str(other_user_post.id), "markup": "Edited post"}},
        auth=user,
    )

    assert result["data"]["postUpdate"] == {
        "updated": False,
        "thread": {
            "id": str(other_user_post.thread_id),
        },
        "post": {
            "id": str(other_user_post.id),
            "richText": [],
        },
        "errors": [
            {
                "location": "post",
                "type": "auth_error.post.not_author",
            },
        ],
    }

    post_from_db = await other_user_post.fetch_from_db()
    assert post_from_db.rich_text == []


@pytest.mark.asyncio
async def test_post_update_mutation_allows_moderator_to_edit_other_user_post(
    query_public_api, moderator, post
):
    result = await query_public_api(
        POST_UPDATE_MUTATION,
        {"input": {"post": str(post.id), "markup": "Edited post"}},
        auth=moderator,
    )

    assert result["data"]["postUpdate"] == {
        "updated": True,
        "thread": {
            "id": str(post.thread_id),
        },
        "post": {
            "id": str(post.id),
            "richText": [
                {
                    "id": ANY,
                    "type": "p",
                    "text": "Edited post",
                },
            ],
        },
        "errors": None,
    }

    post_from_db = await post.fetch_from_db()
    assert post_from_db.rich_text == [
        {
            "id": ANY,
            "type": "p",
            "text": "Edited post",
        }
    ]


@pytest.mark.asyncio
async def test_post_update_mutation_fails_if_thread_is_closed(
    query_public_api, user, closed_user_thread_post
):
    result = await query_public_api(
        POST_UPDATE_MUTATION,
        {"input": {"post": str(closed_user_thread_post.id), "markup": "Edited post"}},
        auth=user,
    )

    assert result["data"]["postUpdate"] == {
        "updated": False,
        "thread": {
            "id": str(closed_user_thread_post.thread_id),
        },
        "post": {
            "id": str(closed_user_thread_post.id),
            "richText": [],
        },
        "errors": [
            {
                "location": "post",
                "type": "auth_error.thread.closed",
            },
        ],
    }

    post_from_db = await closed_user_thread_post.fetch_from_db()
    assert post_from_db.rich_text == []


@pytest.mark.asyncio
async def test_post_update_mutation_allows_moderator_to_post_update_in_closed_thread(
    query_public_api, moderator, closed_user_thread_post
):
    result = await query_public_api(
        POST_UPDATE_MUTATION,
        {"input": {"post": str(closed_user_thread_post.id), "markup": "Edited post"}},
        auth=moderator,
    )

    assert result["data"]["postUpdate"] == {
        "updated": True,
        "thread": {
            "id": str(closed_user_thread_post.thread_id),
        },
        "post": {
            "id": str(closed_user_thread_post.id),
            "richText": [
                {
                    "id": ANY,
                    "type": "p",
                    "text": "Edited post",
                },
            ],
        },
        "errors": None,
    }

    post_from_db = await closed_user_thread_post.fetch_from_db()
    assert post_from_db.rich_text == [
        {
            "id": ANY,
            "type": "p",
            "text": "Edited post",
        }
    ]


@pytest.mark.asyncio
async def test_post_update_mutation_fails_if_category_is_closed(
    query_public_api, user, closed_category_user_post
):
    result = await query_public_api(
        POST_UPDATE_MUTATION,
        {"input": {"post": str(closed_category_user_post.id), "markup": "Edited post"}},
        auth=user,
    )

    assert result["data"]["postUpdate"] == {
        "updated": False,
        "thread": {
            "id": str(closed_category_user_post.thread_id),
        },
        "post": {
            "id": str(closed_category_user_post.id),
            "richText": [],
        },
        "errors": [
            {
                "location": "post",
                "type": "auth_error.category.closed",
            },
        ],
    }

    post_from_db = await closed_category_user_post.fetch_from_db()
    assert post_from_db.rich_text == []


@pytest.mark.asyncio
async def test_post_update_mutation_allows_moderator_to_post_update_in_closed_category(
    query_public_api, moderator, closed_category_user_post
):
    result = await query_public_api(
        POST_UPDATE_MUTATION,
        {"input": {"post": str(closed_category_user_post.id), "markup": "Edited post"}},
        auth=moderator,
    )

    assert result["data"]["postUpdate"] == {
        "updated": True,
        "thread": {
            "id": str(closed_category_user_post.thread_id),
        },
        "post": {
            "id": str(closed_category_user_post.id),
            "richText": [
                {
                    "id": ANY,
                    "type": "p",
                    "text": "Edited post",
                },
            ],
        },
        "errors": None,
    }

    post_from_db = await closed_category_user_post.fetch_from_db()
    assert post_from_db.rich_text == [
        {
            "id": ANY,
            "type": "p",
            "text": "Edited post",
        }
    ]


@pytest.mark.asyncio
async def test_post_update_mutation_fails_if_markup_is_too_short(
    query_public_api, moderator, user_post
):
    result = await query_public_api(
        POST_UPDATE_MUTATION,
        {"input": {"post": str(user_post.id), "markup": "!"}},
        auth=moderator,
    )

    assert result["data"]["postUpdate"] == {
        "updated": False,
        "thread": {
            "id": str(user_post.thread_id),
        },
        "post": {
            "id": str(user_post.id),
            "richText": [],
        },
        "errors": [
            {
                "location": "markup",
                "type": "value_error.any_str.min_length",
            }
        ],
    }

    post_from_db = await user_post.fetch_from_db()
    assert post_from_db.rich_text == []
