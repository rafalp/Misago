import pytest

from .....conf.cache import SETTINGS_CACHE
from .....conf.dynamicsettings import get_settings_from_db
from .....errors import ErrorsList
from .....testing.cacheversions import assert_invalidates_cache
from ..changesettings import resolve_change_settings


@pytest.mark.asyncio
async def test_change_settings_mutation_changes_settings(admin_graphql_info):
    data = await resolve_change_settings(
        None,
        admin_graphql_info,
        input={
            "forumIndexHeader": "New Index Header",
            "forumIndexThreads": False,
            "forumIndexTitle": "New Index Title",
            "forumName": "New Forum Name",
        },
    )

    assert not data.get("errors")
    assert data["settings"] == await get_settings_from_db()
    assert data["settings"]["forum_index_header"] == "New Index Header"
    assert data["settings"]["forum_index_threads"] is False
    assert data["settings"]["forum_index_title"] == "New Index Title"
    assert data["settings"]["forum_name"] == "New Forum Name"


@pytest.mark.asyncio
async def test_change_settings_mutation_invalidates_settings_cache(admin_graphql_info):
    async with assert_invalidates_cache(SETTINGS_CACHE):
        await resolve_change_settings(
            None,
            admin_graphql_info,
            input={
                "forumIndexHeader": "New Index Header",
                "forumIndexThreads": False,
                "forumIndexTitle": "New Index Title",
                "forumName": "New Forum Name",
            },
        )


@pytest.mark.asyncio
async def test_change_settings_mutation_fails_if_user_is_not_admin(user_graphql_info):
    data = await resolve_change_settings(
        None,
        user_graphql_info,
        input={
            "forumIndexHeader": "New Index Header",
            "forumIndexThreads": False,
            "forumIndexTitle": "New Index Title",
            "forumName": "New Forum Name",
        },
    )

    assert data.get("errors")
    assert data["errors"].get_errors_locations() == [ErrorsList.ROOT_LOCATION]
    assert data["errors"].get_errors_types() == ["auth_error.not_admin"]


@pytest.mark.asyncio
async def test_change_settings_mutation_validates_settings_values(admin_graphql_info):
    data = await resolve_change_settings(
        None,
        admin_graphql_info,
        input={
            "forumIndexHeader": "New Index Header",
            "forumIndexThreads": False,
            "forumIndexTitle": "New Index Title",
            "forumName": "",
        },
    )

    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["forumName"]
    assert data["errors"].get_errors_types() == ["value_error.any_str.min_length"]
