import pytest

from ....errors import ErrorsList
from ....threads.get import get_post_by_id, get_thread_by_id
from ..postthread import resolve_post_thread


@pytest.mark.asyncio
async def test_post_thread_mutation_creates_new_thread(
    user_graphql_info, user, category
):
    data = await resolve_post_thread(
        None,
        user_graphql_info,
        input={
            "category": str(category.id),
            "title": "Hello world!",
            "body": "This is test post!",
        },
    )

    assert "errors" not in data
    assert "thread" in data
    assert data["thread"] == await get_thread_by_id(data["thread"].id)
    assert data["thread"].category_id == category.id
    assert data["thread"].starter_id == user.id
    assert data["thread"].starter_name == user.name


@pytest.mark.asyncio
async def test_post_thread_mutation_creates_new_post(user_graphql_info, user, category):
    data = await resolve_post_thread(
        None,
        user_graphql_info,
        input={
            "category": str(category.id),
            "title": "Hello world!",
            "body": "This is test post!",
        },
    )

    assert data["thread"].last_poster_id == user.id
    assert data["thread"].last_poster_name == user.name
    assert data["thread"].first_post_id
    assert data["thread"].first_post_id == data["thread"].last_post_id

    post = await get_post_by_id(data["thread"].first_post_id)
    assert post
    assert post.thread_id == data["thread"].id
    assert post.category_id == category.id
    assert post.poster_id == user.id
    assert post.poster_name == user.name
    assert post.posted_at == data["thread"].started_at
    assert post.posted_at == data["thread"].last_posted_at
    assert post.body == {"text": "This is test post!"}


@pytest.mark.asyncio
async def test_post_thread_mutation_fails_if_user_is_not_authorized(
    graphql_info, category
):
    data = await resolve_post_thread(
        None,
        graphql_info,
        input={
            "category": str(category.id),
            "title": "Hello world!",
            "body": "This is test post!",
        },
    )

    assert "thread" not in data
    assert "errors" in data
    assert data["errors"].get_errors_locations() == [ErrorsList.ROOT_LOCATION]
    assert data["errors"].get_errors_types() == ["auth_error.not_authorized"]
