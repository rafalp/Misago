import pytest

from .....errors import ErrorsList
from .....threads.get import get_post_by_id
from ..deletethreadposts import resolve_delete_thread_posts


@pytest.mark.asyncio
async def test_delete_thread_posts_mutation_deletes_thread_reply(
    moderator_graphql_info, thread_with_reply, thread_reply
):
    data = await resolve_delete_thread_posts(
        None,
        moderator_graphql_info,
        input={"thread": str(thread_with_reply.id), "posts": [str(thread_reply.id)]},
    )

    assert "errors" not in data
    assert data["thread"]
    assert data["deleted"] == [thread_reply.id]
    assert await get_post_by_id(thread_reply.id) is None


@pytest.mark.asyncio
async def test_delete_thread_posts_mutation_fails_if_user_is_not_authorized(
    graphql_info, thread_with_reply, thread_reply
):
    data = await resolve_delete_thread_posts(
        None,
        graphql_info,
        input={"thread": str(thread_with_reply.id), "posts": [str(thread_reply.id)]},
    )

    assert data["thread"] is None
    assert data["errors"]
    assert data["errors"].get_errors_locations() == ["thread", ErrorsList.ROOT_LOCATION]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
        "auth_error.not_authorized",
    ]
    assert data["deleted"] == []


@pytest.mark.asyncio
async def test_delete_thread_posts_mutation_fails_if_user_is_not_moderator(
    user_graphql_info, thread_with_reply, thread_reply
):
    data = await resolve_delete_thread_posts(
        None,
        user_graphql_info,
        input={"thread": str(thread_with_reply.id), "posts": [str(thread_reply.id)]},
    )

    assert data["thread"] is None
    assert data["errors"]
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
    ]
    assert data["deleted"] == []


@pytest.mark.asyncio
async def test_delete_thread_posts_mutation_fails_if_thread_id_is_invalid(
    moderator_graphql_info, thread_reply
):
    data = await resolve_delete_thread_posts(
        None,
        moderator_graphql_info,
        input={"thread": "invalid", "posts": [str(thread_reply.id)]},
    )

    assert data["thread"] is None
    assert data["errors"]
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]
    assert data["deleted"] == []


@pytest.mark.asyncio
async def test_delete_thread_posts_mutation_fails_if_thread_doesnt_exist(
    moderator_graphql_info, thread_reply
):
    data = await resolve_delete_thread_posts(
        None,
        moderator_graphql_info,
        input={"thread": "1000", "posts": [str(thread_reply.id)]},
    )

    assert data["thread"] is None
    assert data["errors"]
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["value_error.thread.not_exists"]
    assert data["deleted"] == []


@pytest.mark.asyncio
async def test_delete_thread_posts_mutation_fails_if_post_id_is_invalid(
    moderator_graphql_info, thread_with_reply, thread_reply
):
    data = await resolve_delete_thread_posts(
        None,
        moderator_graphql_info,
        input={"thread": str(thread_with_reply.id), "posts": ["invalid"]},
    )

    assert data["thread"]
    assert data["errors"]
    assert data["errors"].get_errors_locations() == ["posts.0"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]
    assert data["deleted"] == []


@pytest.mark.asyncio
async def test_delete_thread_posts_mutation_fails_if_post_doesnt_exist(
    moderator_graphql_info, thread_with_reply, thread_reply
):
    data = await resolve_delete_thread_posts(
        None,
        moderator_graphql_info,
        input={
            "thread": str(thread_with_reply.id),
            "posts": [str(thread_reply.id + 1)],
        },
    )

    assert data["thread"]
    assert data["errors"]
    assert data["errors"].get_errors_locations() == ["posts.0"]
    assert data["errors"].get_errors_types() == ["value_error.post.not_exists"]
    assert data["deleted"] == []


@pytest.mark.asyncio
async def test_delete_thread_posts_mutation_fails_if_post_is_threads_first_post(
    moderator_graphql_info, thread, post
):
    data = await resolve_delete_thread_posts(
        None,
        moderator_graphql_info,
        input={"thread": str(thread.id), "posts": [str(post.id)]},
    )

    assert data["thread"]
    assert data["errors"]
    assert data["errors"].get_errors_locations() == ["posts.0"]
    assert data["errors"].get_errors_types() == ["value_error.post.thread_start"]
    assert data["deleted"] == []


@pytest.mark.asyncio
async def test_delete_thread_posts_mutation_fails_if_post_is_in_other_thread(
    moderator_graphql_info, thread_with_reply, other_user_post
):
    data = await resolve_delete_thread_posts(
        None,
        moderator_graphql_info,
        input={
            "thread": str(thread_with_reply.id),
            "posts": [str(other_user_post.id)],
        },
    )

    assert data["thread"]
    assert data["errors"]
    assert data["errors"].get_errors_locations() == ["posts.0"]
    assert data["errors"].get_errors_types() == ["value_error.post.not_exists"]
    assert data["deleted"] == []


@pytest.mark.asyncio
async def test_delete_thread_posts_mutation_with_posts_errors_still_deletes_valid_posts(
    moderator_graphql_info, thread_with_reply, thread_reply, other_user_post
):
    data = await resolve_delete_thread_posts(
        None,
        moderator_graphql_info,
        input={
            "thread": str(thread_with_reply.id),
            "posts": [str(thread_reply.id), str(other_user_post.id)],
        },
    )

    assert data["thread"]
    assert data["errors"]
    assert data["errors"].get_errors_locations() == ["posts.1"]
    assert data["errors"].get_errors_types() == ["value_error.post.not_exists"]
    assert data["deleted"] == [thread_reply.id]
    assert await get_post_by_id(thread_reply.id) is None
    assert await get_post_by_id(other_user_post.id) is not None
