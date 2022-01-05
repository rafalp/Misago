from unittest.mock import ANY

import pytest

from .....conf.cache import SETTINGS_CACHE
from .....conf.dynamicsettings import get_settings_from_db
from .....testing.cacheversions import assert_invalidates_cache
from .....validation import PASSWORD_MAX_LENGTH


def create_query(settings: str) -> str:
    return """
        mutation SettingsUpdate($input: SettingsUpdateInput!) {
            settingsUpdate(input: $input) {
                updated
                settings {
                    %s
                }
                errors {
                    location
                    type
                }
            }
        }
    """ % settings


@pytest.mark.asyncio
async def test_settings_update_mutation_changes_all_settings(query_admin_api):
    query = create_query(
        """
            bulkActionLimit
            enableSiteWizard
            forumIndexHeader
            forumIndexThreads
            forumIndexTitle
            forumName
            jwtExp
            passwordMinLength
            passwordMaxLength
            postMinLength
            postsPerPage
            postsPerPageOrphans
            threadTitleMinLength
            threadTitleMaxLength
            threadsPerPage
            usernameMinLength
            usernameMaxLength
        """
    )

    result = await query_admin_api(
        query,
        {
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
                "usernameMinLength": 7,
                "usernameMaxLength": 14,
            },
        },
    )

    assert result["data"]["settingsUpdate"] == {
        "updated": True,
        "settings": {
            "bulkActionLimit": 5,
            "enableSiteWizard": True,
            "forumIndexHeader": "New Index Header",
            "forumIndexThreads": False,
            "forumIndexTitle": "New Index Title",
            "forumName": "New Forum Name",
            "jwtExp": 5000,
            "passwordMinLength": 15,
            "passwordMaxLength": PASSWORD_MAX_LENGTH,
            "postMinLength": 20,
            "postsPerPage": 15,
            "postsPerPageOrphans": 5,
            "threadTitleMinLength": 3,
            "threadTitleMaxLength": 50,
            "threadsPerPage": 20,
            "usernameMinLength": 7,
            "usernameMaxLength": 14,
        },
        "errors": None,
    }

    settings_from_db = await get_settings_from_db()
    assert settings_from_db["bulk_action_limit"] == 5
    assert settings_from_db["forum_index_header"] == "New Index Header"
    assert settings_from_db["forum_index_threads"] is False
    assert settings_from_db["forum_index_title"] == "New Index Title"
    assert settings_from_db["forum_name"] == "New Forum Name"
    assert settings_from_db["jwt_exp"] == 5000
    assert settings_from_db["password_min_length"] == 15
    assert settings_from_db["post_min_length"] == 20
    assert settings_from_db["posts_per_page"] == 15
    assert settings_from_db["posts_per_page_orphans"] == 5
    assert settings_from_db["thread_title_min_length"] == 3
    assert settings_from_db["thread_title_max_length"] == 50
    assert settings_from_db["threads_per_page"] == 20
    assert settings_from_db["username_min_length"] == 7
    assert settings_from_db["username_max_length"] == 14


@pytest.mark.asyncio
async def test_settings_update_mutation_changes_some_settings(query_admin_api):
    query = create_query(
        """
            bulkActionLimit
            forumIndexThreads
            forumName
            jwtExp
        """
    )

    result = await query_admin_api(
        query,
        {
            "input": {
                "bulkActionLimit": 5,
                "forumIndexThreads": False,
                "jwtExp": 5000,
            },
        },
    )

    assert result["data"]["settingsUpdate"] == {
        "updated": True,
        "settings": {
            "bulkActionLimit": 5,
            "forumIndexThreads": False,
            "forumName": "Misago",
            "jwtExp": 5000,
        },
        "errors": None,
    }

    settings_from_db = await get_settings_from_db()
    assert settings_from_db["bulk_action_limit"] == 5
    assert settings_from_db["forum_index_threads"] is False
    assert settings_from_db["forum_name"] == "Misago"
    assert settings_from_db["jwt_exp"] == 5000


@pytest.mark.asyncio
async def test_settings_update_mutation_invalidates_settings_cache(query_admin_api):
    query = create_query("bulkActionLimit forumName")

    async with assert_invalidates_cache(SETTINGS_CACHE):
        result = await query_admin_api(
            query,
            {
                "input": {
                    "bulkActionLimit": 42,
                    "forumName": "New Forum Name",
                },
            },
        )

        assert result["data"]["settingsUpdate"] == {
            "updated": True,
            "settings": {
                "bulkActionLimit": 42,
                "forumName": "New Forum Name",
            },
            "errors": None,
        }


@pytest.mark.asyncio
async def test_settings_update_mutation_validates_settings_values(query_admin_api):
    query = create_query("forumIndexTitle forumName")

    result = await query_admin_api(
        query,
        {
            "input": {
                "forumIndexTitle": "New Index Title",
                "forumName": "    ",
            },
        },
    )

    assert result["data"]["settingsUpdate"] == {
        "updated": False,
        "settings": {
            "forumIndexTitle": "",
            "forumName": "Misago",
        },
        "errors": [
            {
                "location": ["forumName"],
                "type": "value_error.any_str.min_length",
            },
        ],
    }


@pytest.mark.asyncio
async def test_settings_update_mutation_validates_posts_pagination_bounds(
    query_admin_api,
):
    query = create_query("postsPerPage postsPerPageOrphans")

    result = await query_admin_api(
        query,
        {
            "input": {
                "postsPerPage": 10,
                "postsPerPageOrphans": 26,
            },
        },
    )

    assert result["data"]["settingsUpdate"] == {
        "updated": False,
        "settings": {
            "postsPerPage": 18,
            "postsPerPageOrphans": 6,
        },
        "errors": [
            {
                "location": ["postsPerPage"],
                "type": "value_error.number.not_gt",
            },
            {
                "location": ["postsPerPageOrphans"],
                "type": "value_error.number.not_lt",
            },
        ],
    }


@pytest.mark.asyncio
async def test_settings_update_mutation_validates_thread_title_bounds(query_admin_api):
    query = create_query("threadTitleMinLength threadTitleMaxLength")

    result = await query_admin_api(
        query,
        {
            "input": {
                "threadTitleMinLength": 25,
                "threadTitleMaxLength": 20,
            },
        },
    )

    assert result["data"]["settingsUpdate"] == {
        "updated": False,
        "settings": {
            "threadTitleMinLength": 5,
            "threadTitleMaxLength": 90,
        },
        "errors": [
            {
                "location": ["threadTitleMinLength"],
                "type": "value_error.number.not_lt",
            },
            {
                "location": ["threadTitleMaxLength"],
                "type": "value_error.number.not_gt",
            },
        ],
    }


@pytest.mark.asyncio
async def test_settings_update_mutation_validates_username_bounds(query_admin_api):
    query = create_query("usernameMinLength usernameMaxLength")

    result = await query_admin_api(
        query,
        {
            "input": {
                "usernameMinLength": 5,
                "usernameMaxLength": 2,
            },
        },
    )

    assert result["data"]["settingsUpdate"] == {
        "updated": False,
        "settings": {
            "usernameMinLength": 3,
            "usernameMaxLength": 12,
        },
        "errors": [
            {
                "location": ["usernameMinLength"],
                "type": "value_error.number.not_lt",
            },
            {
                "location": ["usernameMaxLength"],
                "type": "value_error.number.not_gt",
            },
        ],
    }


@pytest.mark.asyncio
async def test_settings_update_mutation_requires_admin_auth(query_admin_api):
    query = create_query("forumName")

    result = await query_admin_api(
        query,
        {
            "input": {
                "forumName": "Test!",
            }
        },
        include_auth=False,
        expect_error=True,
    )

    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None
