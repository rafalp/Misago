import pytest

from .....threads.models import Post
from .....validation import ROOT_LOCATION

POST_DELETE_MUTATION = """
    mutation PostDelete($thread: ID!, $post: ID!) {
        postDelete(thread: $thread, post: $post) {
            deleted
            thread {
                id
            }
            posts {
                results {
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
async def test_post_delete_mutation_deletes_thread_reply(
    query_public_api, moderator, thread_with_reply, thread_reply
):
    result = await query_public_api(
        POST_DELETE_MUTATION,
        {"thread": str(thread_with_reply.id), "post": str(thread_reply.id)},
        auth=moderator,
    )

    assert result["data"]["postDelete"] == {
        "deleted": True,
        "thread": {
            "id": str(thread_with_reply.id),
        },
        "posts": {
            "results": [
                {
                    "id": str(thread_with_reply.first_post_id),
                },
            ],
        },
        "errors": None,
    }

    with pytest.raises(Post.DoesNotExist):
        await thread_reply.fetch_from_db()


@pytest.mark.asyncio
async def test_post_delete_mutation_fails_if_user_is_not_authenticated(
    query_public_api, thread_with_reply, thread_reply
):
    result = await query_public_api(
        POST_DELETE_MUTATION,
        {"thread": str(thread_with_reply.id), "post": str(thread_reply.id)},
    )

    assert result["data"]["postDelete"] == {
        "deleted": False,
        "thread": {
            "id": str(thread_with_reply.id),
        },
        "posts": {
            "results": [
                {
                    "id": str(thread_with_reply.first_post_id),
                },
                {
                    "id": str(thread_reply.id),
                },
            ],
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

    await thread_reply.fetch_from_db()


@pytest.mark.asyncio
async def test_post_delete_mutation_fails_if_user_is_not_moderator(
    query_public_api, user, thread_with_reply, thread_reply
):
    result = await query_public_api(
        POST_DELETE_MUTATION,
        {"thread": str(thread_with_reply.id), "post": str(thread_reply.id)},
        auth=user,
    )

    assert result["data"]["postDelete"] == {
        "deleted": False,
        "thread": {
            "id": str(thread_with_reply.id),
        },
        "posts": {
            "results": [
                {
                    "id": str(thread_with_reply.first_post_id),
                },
                {
                    "id": str(thread_reply.id),
                },
            ],
        },
        "errors": [
            {
                "location": "thread",
                "type": "auth_error.not_moderator",
            },
        ],
    }

    await thread_reply.fetch_from_db()


@pytest.mark.asyncio
async def test_post_delete_mutation_fails_if_thread_id_is_invalid(
    query_public_api, moderator, thread_reply
):
    result = await query_public_api(
        POST_DELETE_MUTATION,
        {"thread": "invalid", "post": str(thread_reply.id)},
        auth=moderator,
    )

    assert result["data"]["postDelete"] == {
        "deleted": False,
        "thread": None,
        "posts": None,
        "errors": [
            {
                "location": "thread",
                "type": "type_error.integer",
            },
        ],
    }

    await thread_reply.fetch_from_db()


@pytest.mark.asyncio
async def test_post_delete_mutation_fails_if_thread_doesnt_exist(
    query_public_api, moderator, thread_reply
):
    result = await query_public_api(
        POST_DELETE_MUTATION,
        {"thread": "1000", "post": str(thread_reply.id)},
        auth=moderator,
    )

    assert result["data"]["postDelete"] == {
        "deleted": False,
        "thread": None,
        "posts": None,
        "errors": [
            {
                "location": "thread",
                "type": "thread_error.not_found",
            },
        ],
    }

    await thread_reply.fetch_from_db()


@pytest.mark.asyncio
async def test_post_delete_mutation_fails_if_post_id_is_invalid(
    query_public_api, moderator, thread_with_reply, thread_reply
):
    result = await query_public_api(
        POST_DELETE_MUTATION,
        {"thread": str(thread_with_reply.id), "post": "invalid"},
        auth=moderator,
    )

    assert result["data"]["postDelete"] == {
        "deleted": False,
        "thread": {
            "id": str(thread_with_reply.id),
        },
        "posts": {
            "results": [
                {
                    "id": str(thread_with_reply.first_post_id),
                },
                {
                    "id": str(thread_reply.id),
                },
            ],
        },
        "errors": [
            {
                "location": "post",
                "type": "type_error.integer",
            },
        ],
    }

    await thread_reply.fetch_from_db()


@pytest.mark.asyncio
async def test_post_delete_mutation_fails_if_post_doesnt_exist(
    query_public_api, moderator, thread_with_reply, thread_reply
):
    result = await query_public_api(
        POST_DELETE_MUTATION,
        {
            "thread": str(thread_with_reply.id),
            "post": str(thread_reply.id + 1),
        },
        auth=moderator,
    )

    assert result["data"]["postDelete"] == {
        "deleted": False,
        "thread": {
            "id": str(thread_with_reply.id),
        },
        "posts": {
            "results": [
                {
                    "id": str(thread_with_reply.first_post_id),
                },
                {
                    "id": str(thread_reply.id),
                },
            ],
        },
        "errors": [
            {
                "location": "post",
                "type": "post_error.not_found",
            },
        ],
    }

    await thread_reply.fetch_from_db()


@pytest.mark.asyncio
async def test_post_delete_mutation_fails_if_post_is_thread_first_post(
    query_public_api, moderator, thread, post
):
    result = await query_public_api(
        POST_DELETE_MUTATION,
        {"thread": str(thread.id), "post": str(post.id)},
        auth=moderator,
    )

    assert result["data"]["postDelete"] == {
        "deleted": False,
        "thread": {
            "id": str(thread.id),
        },
        "posts": {
            "results": [
                {
                    "id": str(post.id),
                },
            ],
        },
        "errors": [
            {
                "location": "post",
                "type": "post_error.thread_start",
            },
        ],
    }

    await post.fetch_from_db()


@pytest.mark.asyncio
async def test_post_delete_mutation_fails_if_post_is_in_other_thread(
    query_public_api, moderator, thread_with_reply, thread_reply, other_user_post
):
    result = await query_public_api(
        POST_DELETE_MUTATION,
        {
            "thread": str(thread_with_reply.id),
            "post": str(other_user_post.id),
        },
        auth=moderator,
    )

    assert result["data"]["postDelete"] == {
        "deleted": False,
        "thread": {
            "id": str(thread_with_reply.id),
        },
        "posts": {
            "results": [
                {
                    "id": str(thread_with_reply.first_post_id),
                },
                {
                    "id": str(thread_reply.id),
                },
            ],
        },
        "errors": [
            {
                "location": "post",
                "type": "post_error.not_found",
            },
        ],
    }

    await other_user_post.fetch_from_db()
