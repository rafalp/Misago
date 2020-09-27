from unittest.mock import ANY

import pytest

from ....pubsub.threads import THREADS_CHANNEL
from ....errors import ErrorsList
from ....testing import override_dynamic_settings
from ....threads.get import get_post_by_id, get_thread_by_id
from ..postthread import resolve_post_thread


@pytest.mark.asyncio
async def test_post_thread_mutation_creates_new_thread(
    publish, user_graphql_info, user, category
):
    data = await resolve_post_thread(
        None,
        user_graphql_info,
        input={
            "category": str(category.id),
            "title": "Hello world!",
            "markup": "This is test post!",
        },
    )

    assert not data.get("errors")
    assert data.get("thread")
    assert data["thread"] == await get_thread_by_id(data["thread"].id)
    assert data["thread"].category_id == category.id
    assert data["thread"].starter_id == user.id
    assert data["thread"].starter_name == user.name
    assert data["thread"].last_poster_id == user.id
    assert data["thread"].last_poster_name == user.name
    assert data["thread"].first_post_id
    assert data["thread"].first_post_id == data["thread"].last_post_id


@pytest.mark.asyncio
async def test_post_thread_mutation_creates_new_post(
    publish, user_graphql_info, user, category
):
    data = await resolve_post_thread(
        None,
        user_graphql_info,
        input={
            "category": str(category.id),
            "title": "Hello world!",
            "markup": "This is test post!",
        },
    )

    assert not data.get("errors")
    assert data.get("post")
    assert data["post"].id == data["thread"].first_post_id
    assert data["post"] == await get_post_by_id(data["thread"].first_post_id)
    assert data["post"].thread_id == data["thread"].id
    assert data["post"].category_id == category.id
    assert data["post"].poster_id == user.id
    assert data["post"].poster_name == user.name
    assert data["post"].posted_at == data["thread"].started_at
    assert data["post"].posted_at == data["thread"].last_posted_at
    assert data["post"].body == {"text": "This is test post!"}


@pytest.mark.asyncio
async def test_post_thread_mutation_publishes_thread_updated_event(
    publish, user_graphql_info, category
):
    await resolve_post_thread(
        None,
        user_graphql_info,
        input={
            "category": str(category.id),
            "title": "Hello world!",
            "markup": "This is test post!",
        },
    )

    publish.assert_called_once_with(channel=THREADS_CHANNEL, message=ANY)


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
            "markup": "This is test post!",
        },
    )

    assert not data.get("thread")
    assert not data.get("post")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == [ErrorsList.ROOT_LOCATION]
    assert data["errors"].get_errors_types() == ["auth_error.not_authorized"]


@pytest.mark.asyncio
async def test_post_thread_mutation_fails_if_category_id_is_invalid(user_graphql_info):
    data = await resolve_post_thread(
        None,
        user_graphql_info,
        input={
            "category": "invalid",
            "title": "Hello world!",
            "markup": "This is test post!",
        },
    )

    assert not data.get("thread")
    assert not data.get("post")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["category"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_post_thread_mutation_fails_if_category_doesnt_exist(user_graphql_info):
    data = await resolve_post_thread(
        None,
        user_graphql_info,
        input={
            "category": "4000",
            "title": "Hello world!",
            "markup": "This is test post!",
        },
    )

    assert not data.get("thread")
    assert not data.get("post")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["category"]
    assert data["errors"].get_errors_types() == ["value_error.category.not_exists"]


@pytest.mark.asyncio
@override_dynamic_settings(thread_title_min_length=5)
async def test_post_thread_mutation_validates_min_title_length(
    user_graphql_info, category
):
    data = await resolve_post_thread(
        None,
        user_graphql_info,
        input={
            "category": str(category.id),
            "title": "Test",
            "markup": "This is test post!",
        },
    )

    assert not data.get("thread")
    assert not data.get("post")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["title"]
    assert data["errors"].get_errors_types() == ["value_error.any_str.min_length"]


@pytest.mark.asyncio
@override_dynamic_settings(thread_title_max_length=10)
async def test_post_thread_mutation_validates_max_title_length(
    user_graphql_info, category
):
    data = await resolve_post_thread(
        None,
        user_graphql_info,
        input={
            "category": str(category.id),
            "title": "a" * 11,
            "markup": "This is test post!",
        },
    )

    assert not data.get("thread")
    assert not data.get("post")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["title"]
    assert data["errors"].get_errors_types() == ["value_error.any_str.max_length"]


@pytest.mark.asyncio
async def test_post_thread_mutation_validates_title_contains_alphanumeric_characters(
    user_graphql_info, category
):
    data = await resolve_post_thread(
        None,
        user_graphql_info,
        input={
            "category": str(category.id),
            "title": "!" * 10,
            "markup": "This is test post!",
        },
    )

    assert not data.get("thread")
    assert not data.get("post")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["title"]
    assert data["errors"].get_errors_types() == ["value_error.str.regex"]


@pytest.mark.asyncio
async def test_post_thread_mutation_fails_if_category_is_closed(
    user_graphql_info, closed_category
):
    data = await resolve_post_thread(
        None,
        user_graphql_info,
        input={
            "category": str(closed_category.id),
            "title": "Hello world!",
            "markup": "This is test post!",
        },
    )

    assert not data.get("thread")
    assert not data.get("post")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["category"]
    assert data["errors"].get_errors_types() == ["auth_error.category.closed"]


@pytest.mark.asyncio
async def test_post_thread_mutation_allows_moderator_to_post_thread_in_closed_category(
    publish, moderator_graphql_info, closed_category
):
    data = await resolve_post_thread(
        None,
        moderator_graphql_info,
        input={
            "category": str(closed_category.id),
            "title": "Hello world!",
            "markup": "This is test post!",
        },
    )

    assert not data.get("errors")
    assert data.get("thread")
    assert data.get("post")


@pytest.mark.asyncio
async def test_post_thread_mutation_creates_open_thread(
    publish, user_graphql_info, category
):
    data = await resolve_post_thread(
        None,
        user_graphql_info,
        input={
            "category": str(category.id),
            "title": "Hello world!",
            "markup": "This is test post!",
            "is_closed": False,
        },
    )

    assert not data.get("errors")
    assert data.get("thread")
    assert data["thread"] == await get_thread_by_id(data["thread"].id)
    assert not data["thread"].is_closed


@pytest.mark.asyncio
async def test_post_thread_mutation_allows_moderator_to_post_closed_thread(
    publish, moderator_graphql_info, category
):
    data = await resolve_post_thread(
        None,
        moderator_graphql_info,
        input={
            "category": str(category.id),
            "title": "Hello world!",
            "markup": "This is test post!",
            "is_closed": True,
        },
    )

    assert not data.get("errors")
    assert data.get("thread")
    assert data["thread"] == await get_thread_by_id(data["thread"].id)
    assert data["thread"].is_closed


@pytest.mark.asyncio
async def test_post_thread_mutation_fails_if_non_moderator_posts_closed_thread(
    publish, user_graphql_info, category
):
    data = await resolve_post_thread(
        None,
        user_graphql_info,
        input={
            "category": str(category.id),
            "title": "Hello world!",
            "markup": "This is test post!",
            "is_closed": True,
        },
    )

    assert not data.get("thread")
    assert not data.get("post")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["isClosed"]
    assert data["errors"].get_errors_types() == ["auth_error.not_moderator"]
