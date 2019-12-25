import pytest

from ....errors import ErrorsList
from ....threads.get import get_post_by_id, get_thread_by_id
from ..postreply import resolve_post_reply


@pytest.mark.asyncio
async def test_post_reply_mutation_creates_new_reply(user_graphql_info, user, thread):
    data = await resolve_post_reply(
        None,
        user_graphql_info,
        input={"thread": str(thread.id), "body": "This is test post!",},
    )

    assert not data.get("errors")
    assert data.get("post")
    assert data["post"] == await get_post_by_id(data["post"].id)
    assert data["post"].thread_id == data["thread"].id
    assert data["post"].category_id == thread.category_id
    assert data["post"].poster_id == user.id
    assert data["post"].poster_name == user.name
    assert data["post"].posted_at != data["thread"].started_at
    assert data["post"].posted_at == data["thread"].last_posted_at
    assert data["post"].body == {"text": "This is test post!"}


@pytest.mark.asyncio
async def test_post_reply_mutation_updates_thread(user_graphql_info, user, thread):
    data = await resolve_post_reply(
        None,
        user_graphql_info,
        input={"thread": str(thread.id), "body": "This is test post!",},
    )

    assert not data.get("errors")
    assert data.get("thread")
    assert data["post"].id == data["thread"].last_post_id
    assert data["thread"] == await get_thread_by_id(data["thread"].id)
    assert data["thread"].last_post_id != data["thread"].first_post_id
    assert data["thread"].id == thread.id
    assert data["thread"].starter_id != user.id
    assert data["thread"].starter_name != user.name
    assert data["thread"].last_poster_id == user.id
    assert data["thread"].last_poster_name == user.name
    assert data["thread"].last_posted_at > thread.last_posted_at
    assert data["thread"].replies > thread.replies


@pytest.mark.asyncio
async def test_post_reply_mutation_fails_if_user_is_not_authorized(
    graphql_info, thread
):
    data = await resolve_post_reply(
        None,
        graphql_info,
        input={"thread": str(thread.id), "body": "This is test post!",},
    )

    assert data.get("thread")
    assert not data.get("post")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == [ErrorsList.ROOT_LOCATION]
    assert data["errors"].get_errors_types() == ["auth_error.not_authorized"]


@pytest.mark.asyncio
async def test_post_reply_mutation_fails_if_thread_id_is_invalid(user_graphql_info):
    data = await resolve_post_reply(
        None,
        user_graphql_info,
        input={"thread": "invalid", "body": "This is test post!",},
    )

    assert not data.get("thread")
    assert not data.get("post")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_post_reply_mutation_fails_if_thread_doesnt_exist(user_graphql_info):
    data = await resolve_post_reply(
        None,
        user_graphql_info,
        input={"thread": "4000", "body": "This is test post!",},
    )

    assert not data.get("thread")
    assert not data.get("post")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["value_error.thread.not_exists"]


@pytest.mark.asyncio
async def test_post_reply_mutation_fails_if_thread_is_closed(
    user_graphql_info, closed_thread
):
    data = await resolve_post_reply(
        None,
        user_graphql_info,
        input={"thread": str(closed_thread.id), "body": "This is test post!",},
    )

    assert data.get("thread")
    assert not data.get("post")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["auth_error.thread.closed"]


@pytest.mark.asyncio
async def test_post_reply_mutation_allows_moderator_to_post_reply_in_closed_thread(
    moderator_graphql_info, closed_thread
):
    data = await resolve_post_reply(
        None,
        moderator_graphql_info,
        input={"thread": str(closed_thread.id), "body": "This is test post!",},
    )

    assert data.get("thread")
    assert data.get("post")
    assert not data.get("errors")


@pytest.mark.asyncio
async def test_post_reply_mutation_fails_if_category_is_closed(
    user_graphql_info, closed_category_thread
):
    data = await resolve_post_reply(
        None,
        user_graphql_info,
        input={"thread": str(closed_category_thread.id), "body": "This is test post!",},
    )

    assert data.get("thread")
    assert not data.get("post")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["auth_error.category.closed"]


@pytest.mark.asyncio
async def test_post_reply_mutation_allows_moderator_to_post_reply_in_closed_category(
    moderator_graphql_info, closed_category_thread
):
    data = await resolve_post_reply(
        None,
        moderator_graphql_info,
        input={"thread": str(closed_category_thread.id), "body": "This is test post!",},
    )

    assert data.get("thread")
    assert data.get("post")
    assert not data.get("errors")
