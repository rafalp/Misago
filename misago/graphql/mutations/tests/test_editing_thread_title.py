import pytest

from ....errors import ErrorsList
from ....threads.get import get_thread_by_id
from ..editthreadtitle import resolve_edit_thread_title


@pytest.mark.asyncio
async def test_edit_title_mutation_updates_thread(user_graphql_info, user, user_thread):
    data = await resolve_edit_thread_title(
        None,
        user_graphql_info,
        input={"thread": str(user_thread.id), "title": "Edited thread"},
    )

    assert not data.get("errors")
    assert data.get("thread")
    assert data["thread"] == await get_thread_by_id(data["thread"].id)
    assert data["thread"].title == "Edited thread"
    assert data["thread"].slug == "edited-thread"


@pytest.mark.asyncio
async def test_edit_title_mutation_fails_if_user_is_not_authorized(
    graphql_info, user_thread
):
    data = await resolve_edit_thread_title(
        None,
        graphql_info,
        input={"thread": str(user_thread.id), "title": "Edited thread"},
    )

    assert not data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == [ErrorsList.ROOT_LOCATION]
    assert data["errors"].get_errors_types() == ["auth_error.not_authorized"]


@pytest.mark.asyncio
async def test_edit_title_mutation_fails_if_thread_id_is_invalid(user_graphql_info):
    data = await resolve_edit_thread_title(
        None,
        user_graphql_info,
        input={"thread": "invalid", "title": "This is test thread!"},
    )

    assert not data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_edit_title_mutation_fails_if_thread_doesnt_exist(user_graphql_info):
    data = await resolve_edit_thread_title(
        None,
        user_graphql_info,
        input={"thread": "4000", "title": "This is test thread!"},
    )

    assert not data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["value_error.thread_does_not_exist"]


@pytest.mark.asyncio
async def test_edit_title_mutation_fails_if_thread_author_is_other_user(
    user_graphql_info, other_user_thread
):
    data = await resolve_edit_thread_title(
        None,
        user_graphql_info,
        input={"thread": str(other_user_thread.id), "title": "This is test thread!"},
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["auth_error.not_thread_author_error"]


@pytest.mark.asyncio
async def test_edit_title_mutation_allowss_moderator_to_edit_other_user_thread(
    moderator_graphql_info, other_user_thread
):
    data = await resolve_edit_thread_title(
        None,
        moderator_graphql_info,
        input={"thread": str(other_user_thread.id), "title": "This is test thread!"},
    )

    assert data.get("thread")
    assert not data.get("errors")


@pytest.mark.asyncio
async def test_edit_title_mutation_fails_if_thread_is_closed(
    user_graphql_info, closed_user_thread
):
    data = await resolve_edit_thread_title(
        None,
        user_graphql_info,
        input={"thread": str(closed_user_thread.id), "title": "This is test thread!",},
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["auth_error.thread_is_closed"]


@pytest.mark.asyncio
async def test_edit_title_mutation_allows_moderator_to_edit_title_in_closed_thread(
    moderator_graphql_info, closed_user_thread
):
    data = await resolve_edit_thread_title(
        None,
        moderator_graphql_info,
        input={"thread": str(closed_user_thread.id), "title": "This is test thread!",},
    )

    assert data.get("thread")
    assert not data.get("errors")


@pytest.mark.asyncio
async def test_edit_title_mutation_fails_if_category_is_closed(
    user_graphql_info, closed_category_user_thread
):
    data = await resolve_edit_thread_title(
        None,
        user_graphql_info,
        input={
            "thread": str(closed_category_user_thread.id),
            "title": "This is test thread!",
        },
    )

    assert data.get("thread")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["thread"]
    assert data["errors"].get_errors_types() == ["auth_error.category_is_closed"]


@pytest.mark.asyncio
async def test_edit_title_mutation_allows_moderator_to_edit_title_in_closed_category(
    moderator_graphql_info, closed_category_user_thread
):
    data = await resolve_edit_thread_title(
        None,
        moderator_graphql_info,
        input={
            "thread": str(closed_category_user_thread.id),
            "title": "This is test thread!",
        },
    )

    assert data.get("thread")
    assert not data.get("errors")
