import pytest

from ....errors import ErrorsList
from ....threads.get import get_thread_by_id
from ..movethread import resolve_move_thread


@pytest.mark.asyncio
async def test_move_thread_mutation_moves_thread(
    moderator_graphql_info, thread, sibling_category
):
    data = await resolve_move_thread(
        None,
        moderator_graphql_info,
        input={"thread": str(thread.id), "category": str(sibling_category.id)},
    )

    assert not data.get("errors")
    assert data.get("thread")
    assert data["thread"] == await get_thread_by_id(data["thread"].id)
    assert data["thread"].category_id == sibling_category.id


@pytest.mark.asyncio
async def test_move_thread_mutation_fails_if_user_is_not_authorized(
    graphql_info, thread, sibling_category
):
    data = await resolve_move_thread(
        None,
        graphql_info,
        input={"thread": str(thread.id), "category": str(sibling_category.id)},
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread", ErrorsList.ROOT_LOCATION]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
        "auth_error.not_authorized",
    ]


@pytest.mark.asyncio
async def test_move_thread_mutation_fails_if_user_is_not_moderator(
    user_graphql_info, thread, sibling_category
):
    data = await resolve_move_thread(
        None,
        user_graphql_info,
        input={"thread": str(thread.id), "category": str(sibling_category.id)},
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == [
        "auth_error.not_moderator",
    ]


@pytest.mark.asyncio
async def test_move_thread_mutation_fails_if_thread_id_is_invalid(
    moderator_graphql_info, sibling_category
):
    data = await resolve_move_thread(
        None,
        moderator_graphql_info,
        input={"thread": "invalid", "category": str(sibling_category.id)},
    )

    assert not data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_move_thread_mutation_fails_if_thread_doesnt_exist(
    moderator_graphql_info, sibling_category
):
    data = await resolve_move_thread(
        None,
        moderator_graphql_info,
        input={"thread": "4000", "category": str(sibling_category.id)},
    )

    assert not data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["value_error.thread_does_not_exist"]


@pytest.mark.asyncio
async def test_move_thread_mutation_fails_if_category_id_is_invalid(
    moderator_graphql_info, thread
):
    data = await resolve_move_thread(
        None,
        moderator_graphql_info,
        input={"thread": str(thread.id), "category": "invalid"},
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["category"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_move_thread_mutation_fails_if_category_doesnt_exist(
    moderator_graphql_info, thread
):
    data = await resolve_move_thread(
        None,
        moderator_graphql_info,
        input={"thread": str(thread.id), "category": "1000"},
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["category"]
    assert data["errors"].get_errors_types() == ["value_error.category_does_not_exist"]
