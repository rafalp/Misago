import pytest

SETTINGS_QUERY = """
    query Settings {
        settings {
            bulkActionLimit
            enableSiteWizard
            forumIndexThreads
            forumIndexTitle
            forumName
            jwtExp
            passwordMinLength
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
async def test_settings_query_returns_settings(query_admin_api):
    result = await query_admin_api(SETTINGS_QUERY)
    assert result["data"]["settings"]


@pytest.mark.asyncio
async def test_settings_query_requires_admin_auth(query_admin_api):
    result = await query_admin_api(
        SETTINGS_QUERY, expect_error=True, include_auth=False
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"]["settings"] is None
