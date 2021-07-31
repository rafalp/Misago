import pytest

from .....conf.cache import SETTINGS_CACHE
from .....conf.dynamicsettings import get_settings_from_db
from .....errors import ErrorsList
from .....testing.cacheversions import assert_invalidates_cache

SETTINGS_UPDATE_MUTATION = """
    mutation SettingsUpdate($input: SettingsUpdateInput!) {
        settingsUpdate(input: $input) {
            updated
            errors {
                location
                type
            }
            settings {
                bulkActionLimit
                enableSiteWizard
                forumIndexHeader
                forumIndexThreads
                forumIndexTitle
                forumName
                passwordMinLength
                passwordMaxLength
                postMinLength
                threadTitleMinLength
                threadTitleMaxLength
                usernameMinLength
                usernameMaxLength
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_change_settings_mutation_changes_settings(query_admin_api):
    variables = {
        "input": {
            "bulkActionLimit": 5,
            "forumIndexHeader": "New Index Header",
            "forumIndexThreads": False,
            "forumIndexTitle": "New Index Title",
            "forumName": "New Forum Name",
            "jwtExp": 5000,
            "passwordMinLength": 15,
            "postMinLength": 20,
            "postsPerPage": 15,
            "postsPerPageOrphans": 5,
            "threadTitleMinLength": 3,
            "threadTitleMaxLength": 50,
            "threadsPerPage": 20,
        }
    }

    result = await query_admin_api(SETTINGS_UPDATE_MUTATION, variables)
    data = result["data"]["settingsUpdate"]

    assert not data["errors"]
    assert data["updated"]
    assert data["settings"]["forumIndexHeader"] == "New Index Header"
    assert data["settings"]["forumIndexThreads"] is False
    assert data["settings"]["forumIndexTitle"] == "New Index Title"
    assert data["settings"]["forumName"] == "New Forum Name"

    updated_settings = await get_settings_from_db()
    assert updated_settings["bulk_action_limit"] == 5
    assert updated_settings["forum_index_header"] == "New Index Header"
    assert updated_settings["forum_index_threads"] is False
    assert updated_settings["forum_index_title"] == "New Index Title"
    assert updated_settings["forum_name"] == "New Forum Name"
    assert updated_settings["jwt_exp"] == 5000
    assert updated_settings["password_min_length"] == 15
    assert updated_settings["post_min_length"] == 20
    assert updated_settings["posts_per_page"] == 15
    assert updated_settings["posts_per_page_orphans"] == 5
    assert updated_settings["thread_title_min_length"] == 3
    assert updated_settings["thread_title_max_length"] == 50
    assert updated_settings["threads_per_page"] == 20


@pytest.mark.asyncio
async def test_change_settings_mutation_changes_some_settings(query_admin_api):
    variables = {
        "input": {
            "bulkActionLimit": 5,
            "forumIndexThreads": False,
            "jwtExp": 5000,
        }
    }

    result = await query_admin_api(SETTINGS_UPDATE_MUTATION, variables)
    data = result["data"]["settingsUpdate"]

    assert not data["errors"]
    assert data["updated"]
    assert data["settings"]["forumIndexThreads"] is False

    updated_settings = await get_settings_from_db()
    assert updated_settings["bulk_action_limit"] == 5
    assert updated_settings["forum_index_threads"] is False
    assert updated_settings["jwt_exp"] == 5000


@pytest.mark.asyncio
async def test_change_settings_mutation_invalidates_settings_cache(query_admin_api):
    async with assert_invalidates_cache(SETTINGS_CACHE):
        variables = {
            "input": {
                "forumIndexHeader": "New Index Header",
                "forumIndexThreads": False,
                "forumIndexTitle": "New Index Title",
                "forumName": "New Forum Name",
            }
        }

        result = await query_admin_api(SETTINGS_UPDATE_MUTATION, variables)
        data = result["data"]["settingsUpdate"]
        assert not data["errors"]
        assert data["updated"]


@pytest.mark.asyncio
async def test_change_settings_mutation_validates_settings_values(query_admin_api):
    variables = {
        "input": {
            "forumIndexHeader": "New Index Header",
            "forumIndexThreads": False,
            "forumIndexTitle": "New Index Title",
            "forumName": "    ",
        }
    }

    result = await query_admin_api(SETTINGS_UPDATE_MUTATION, variables)
    data = result["data"]["settingsUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {"location": ["forumName"], "type": "value_error.any_str.min_length"}
    ]


@pytest.mark.asyncio
async def test_change_settings_mutation_fails_if_user_is_not_admin(query_admin_api):
    variables = {
        "input": {
            "forumIndexHeader": "New Index Header",
            "forumIndexThreads": False,
            "forumIndexTitle": "New Index Title",
            "forumName": "New Forum Name",
        }
    }

    result = await query_admin_api(
        SETTINGS_UPDATE_MUTATION, variables, include_auth=False
    )
    data = result["data"]["settingsUpdate"]

    assert data["errors"] == [
        {"location": [ErrorsList.ROOT_LOCATION], "type": "auth_error.not_admin"}
    ]


@pytest.mark.asyncio
async def test_change_settings_mutation_validates_posts_pagination_bounds(
    query_admin_api,
):
    variables = {
        "input": {
            "postsPerPage": 20,
            "postsPerPageOrphans": 25,
        }
    }

    result = await query_admin_api(SETTINGS_UPDATE_MUTATION, variables)
    data = result["data"]["settingsUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {"location": ["postsPerPage"], "type": "value_error.number.not_gt"},
        {"location": ["postsPerPageOrphans"], "type": "value_error.number.not_lt"},
    ]


@pytest.mark.asyncio
async def test_change_settings_mutation_validates_thread_title_bounds(query_admin_api):
    variables = {
        "input": {
            "threadTitleMinLength": 25,
            "threadTitleMaxLength": 20,
        }
    }

    result = await query_admin_api(SETTINGS_UPDATE_MUTATION, variables)
    data = result["data"]["settingsUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {"location": ["threadTitleMinLength"], "type": "value_error.number.not_lt"},
        {"location": ["threadTitleMaxLength"], "type": "value_error.number.not_gt"},
    ]


@pytest.mark.asyncio
async def test_change_settings_mutation_validates_username_bounds(query_admin_api):
    variables = {
        "input": {
            "usernameMinLength": 5,
            "usernameMaxLength": 2,
        }
    }

    result = await query_admin_api(SETTINGS_UPDATE_MUTATION, variables)
    data = result["data"]["settingsUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {"location": ["usernameMinLength"], "type": "value_error.number.not_lt"},
        {"location": ["usernameMaxLength"], "type": "value_error.number.not_gt"},
    ]
