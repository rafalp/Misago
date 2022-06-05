import pytest


PLUGINS_QUERY = """
    query {
        plugins {
            name
            description
            license
            icon
            color
            version
            author
            homepage {
                domain
                url
            }
            repo {
                domain
                icon
                url
            }
            directory
            admin
            client
        }
    }
"""


@pytest.mark.asyncio
async def test_admin_schema_plugins_query_returns_plugins_list(query_admin_api, admin):
    result = await query_admin_api(PLUGINS_QUERY)
    assert result["data"]["plugins"]


@pytest.mark.asyncio
async def test_admin_schema_plugins_query_requires_admin_auth(query_admin_api):
    result = await query_admin_api(
        PLUGINS_QUERY,
        expect_error=True,
        include_auth=False,
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None
