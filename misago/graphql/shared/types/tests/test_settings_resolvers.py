import pytest

from .....validation import PASSWORD_MAX_LENGTH


@pytest.mark.asyncio
async def test_query_settings_resolver_returns_settings_from_context(
    query_public_api, dynamic_settings
):
    query = """
        query GetSettings {
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
    """

    result = await query_public_api(query)
    assert result["data"]["settings"] == {
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
