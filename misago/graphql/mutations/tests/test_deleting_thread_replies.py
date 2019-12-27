import pytest

from ....errors import ErrorsList
from ....threads.get import get_post_by_id
from ..deletethreadreplies import resolve_delete_thread_replies


@pytest.mark.asyncio
async def test_delete_thread_replies_mutation_deletes_thread_reply(
    moderator_graphql_info, thread_with_reply, thread_reply
):
    data = await resolve_delete_thread_replies(
        None,
        moderator_graphql_info,
        input={"thread": str(thread_with_reply.id), "replies": [str(thread_reply.id)]},
    )

    assert data.get("thread")
    assert not data.get("errors")
    assert await get_post_by_id(thread_reply.id) is None


@pytest.mark.asyncio
async def test_delete_thread_replies_mutation_fails_if_user_is_not_authorized(
    graphql_info, thread_with_reply, thread_reply
):
    data = await resolve_delete_thread_replies(
        None,
        graphql_info,
        input={"thread": str(thread_with_reply.id), "replies": [str(thread_reply.id)]},
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread", ErrorsList.ROOT_LOCATION]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
        "auth_error.not_authorized",
    ]


@pytest.mark.asyncio
async def test_delete_thread_replies_mutation_fails_if_user_is_not_moderator(
    user_graphql_info, thread_with_reply, thread_reply
):
    data = await resolve_delete_thread_replies(
        None,
        user_graphql_info,
        input={"thread": str(thread_with_reply.id), "replies": [str(thread_reply.id)]},
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
    ]


@pytest.mark.asyncio
async def test_delete_thread_replies_mutation_fails_if_thread_id_is_invalid(
    moderator_graphql_info, thread_reply
):
    data = await resolve_delete_thread_replies(
        None,
        moderator_graphql_info,
        input={"thread": "invalid", "replies": [str(thread_reply.id)]},
    )

    assert not data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_delete_thread_replies_mutation_fails_if_thread_doesnt_exist(
    moderator_graphql_info, thread_reply
):
    data = await resolve_delete_thread_replies(
        None,
        moderator_graphql_info,
        input={"thread": "1000", "replies": [str(thread_reply.id)]},
    )

    assert not data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["value_error.thread.not_exists"]


@pytest.mark.asyncio
async def test_delete_thread_replies_mutation_fails_if_reply_id_is_invalid(
    moderator_graphql_info, thread_with_reply, thread_reply
):
    data = await resolve_delete_thread_replies(
        None,
        moderator_graphql_info,
        input={"thread": str(thread_with_reply.id), "replies": ["invalid"]},
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["replies.0"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_delete_thread_replies_mutation_fails_if_reply_doesnt_exist(
    moderator_graphql_info, thread_with_reply, thread_reply
):
    data = await resolve_delete_thread_replies(
        None,
        moderator_graphql_info,
        input={
            "thread": str(thread_with_reply.id),
            "replies": [str(thread_reply.id + 1)],
        },
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["replies.0"]
    assert data["errors"].get_errors_types() == ["value_error.post.not_exists"]


@pytest.mark.asyncio
async def test_delete_thread_replies_mutation_fails_if_reply_is_threads_first_post(
    moderator_graphql_info, thread, post
):
    data = await resolve_delete_thread_replies(
        None,
        moderator_graphql_info,
        input={"thread": str(thread.id), "replies": [str(post.id)]},
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["replies.0"]
    assert data["errors"].get_errors_types() == ["value_error.post.thread_start"]


@pytest.mark.asyncio
async def test_delete_thread_replies_mutation_fails_if_reply_is_in_other_thread(
    moderator_graphql_info, thread_with_reply, other_user_post
):
    data = await resolve_delete_thread_replies(
        None,
        moderator_graphql_info,
        input={
            "thread": str(thread_with_reply.id),
            "replies": [str(other_user_post.id)],
        },
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["replies.0"]
    assert data["errors"].get_errors_types() == ["value_error.post.not_exists"]
