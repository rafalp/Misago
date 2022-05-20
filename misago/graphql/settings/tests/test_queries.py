import pytest

from ....conf import settings
from ....users.validators import PASSWORD_MAX_LENGTH

SETTINGS_QUERY = """
    query GetSettings {
        settings {
            avatarUploadContentTypes
            avatarUploadImageMinSize
            avatarUploadMaxSize
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
"""


@pytest.mark.asyncio
async def test_settings_query_returns_settings(query_public_api, dynamic_settings):
    result = await query_public_api(SETTINGS_QUERY)
    assert result["data"]["settings"] == {
        "avatarUploadContentTypes": list(settings.avatar_content_types),
        "avatarUploadImageMinSize": max(settings.avatar_sizes),
        "avatarUploadMaxSize": dynamic_settings["avatar_upload_max_size"],
        "bulkActionLimit": dynamic_settings["bulk_action_limit"],
        "enableSiteWizard": dynamic_settings["enable_site_wizard"],
        "forumIndexHeader": dynamic_settings["forum_index_header"],
        "forumIndexThreads": dynamic_settings["forum_index_threads"],
        "forumIndexTitle": dynamic_settings["forum_index_title"],
        "forumName": dynamic_settings["forum_name"],
        "passwordMinLength": dynamic_settings["password_min_length"],
        "passwordMaxLength": PASSWORD_MAX_LENGTH,
        "postMinLength": dynamic_settings["post_min_length"],
        "threadTitleMinLength": dynamic_settings["thread_title_min_length"],
        "threadTitleMaxLength": dynamic_settings["thread_title_max_length"],
        "usernameMinLength": dynamic_settings["username_min_length"],
        "usernameMaxLength": dynamic_settings["username_max_length"],
    }


ADMIN_SETTINGS_QUERY = """
    query Settings {
        settings {
            avatarUploadContentTypes
            avatarUploadImageMinSize
            avatarUploadMaxSize
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
        }
    }
"""


@pytest.mark.asyncio
async def test_admin_settings_query_returns_settings(query_admin_api, dynamic_settings):
    result = await query_admin_api(ADMIN_SETTINGS_QUERY)
    assert result["data"]["settings"] == {
        "avatarUploadContentTypes": list(settings.avatar_content_types),
        "avatarUploadImageMinSize": max(settings.avatar_sizes),
        "avatarUploadMaxSize": dynamic_settings["avatar_upload_max_size"],
        "bulkActionLimit": dynamic_settings["bulk_action_limit"],
        "enableSiteWizard": dynamic_settings["enable_site_wizard"],
        "forumIndexHeader": dynamic_settings["forum_index_header"],
        "forumIndexThreads": dynamic_settings["forum_index_threads"],
        "forumIndexTitle": dynamic_settings["forum_index_title"],
        "forumName": dynamic_settings["forum_name"],
        "jwtExp": dynamic_settings["jwt_exp"],
        "passwordMinLength": dynamic_settings["password_min_length"],
        "passwordMaxLength": PASSWORD_MAX_LENGTH,
        "postMinLength": dynamic_settings["post_min_length"],
        "postsPerPage": dynamic_settings["posts_per_page"],
        "postsPerPageOrphans": dynamic_settings["posts_per_page_orphans"],
        "threadTitleMinLength": dynamic_settings["thread_title_min_length"],
        "threadTitleMaxLength": dynamic_settings["thread_title_max_length"],
        "threadsPerPage": dynamic_settings["threads_per_page"],
        "usernameMinLength": dynamic_settings["username_min_length"],
        "usernameMaxLength": dynamic_settings["username_max_length"],
    }


@pytest.mark.asyncio
async def test_admin_settings_query_requires_admin_auth(query_admin_api):
    result = await query_admin_api(
        ADMIN_SETTINGS_QUERY, expect_error=True, include_auth=False
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"]["settings"] is None
