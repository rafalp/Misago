import pytest

from .....errors import ErrorsList
from .....threads.models import Post


POST_DELETE_MUTATION = """
    mutation PostDelete($thread: ID!, $post: ID!) {
        postDelete(thread: $thread, post: $post) {
            deleted
            thread {
                id
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
        "errors": None,
    }

    with pytest.raises(Post.DoesNotExist):
        await thread_reply.refresh_from_db()


@pytest.mark.asyncio
async def test_post_delete_mutation_fails_if_user_is_not_authorized(
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

    await thread_reply.refresh_from_db()


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
        "errors": [
            {
                "location": "thread",
                "type": "auth_error.not_moderator",
            },
        ],
    }

    await thread_reply.refresh_from_db()


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
        "errors": [
            {
                "location": "thread",
                "type": "type_error.integer",
            },
        ],
    }

    await thread_reply.refresh_from_db()


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
        "errors": [
            {
                "location": "thread",
                "type": "value_error.thread.not_exists",
            },
        ],
    }

    await thread_reply.refresh_from_db()


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
        "errors": [
            {
                "location": "post",
                "type": "type_error.integer",
            },
        ],
    }

    await thread_reply.refresh_from_db()


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
        "errors": [
            {
                "location": "post",
                "type": "value_error.post.not_exists",
            },
        ],
    }

    await thread_reply.refresh_from_db()


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
        "errors": [
            {
                "location": "post",
                "type": "value_error.post.thread_start",
            },
        ],
    }

    await post.refresh_from_db()


@pytest.mark.asyncio
async def test_post_delete_mutation_fails_if_post_is_in_other_thread(
    query_public_api, moderator, thread_with_reply, other_user_post
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
        "errors": [
            {
                "location": "post",
                "type": "value_error.post.not_exists",
            },
        ],
    }

    await other_user_post.refresh_from_db()
