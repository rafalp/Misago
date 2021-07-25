import pytest


@pytest.mark.asyncio
async def test_users_query_returns_list_of_users(query_admin_api, admin):
    result = await query_admin_api(
        """
            {
                users {
                    page {
                        items {
                            id
                        }
                    }
                }
            }
        """
    )

    assert "errors" not in result
    assert result["data"]["users"]["page"]["items"] == [{"id": str(admin.id)}]


FILTER_USERS_QUERY = """
    query Users($filters: UsersFilters) {
        users(filters: $filters) {
            page {
                items {
                    id
                }
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_users_query_filters_names(query_admin_api, other_user):
    result = await query_admin_api(FILTER_USERS_QUERY, {"filters": {"name": "Other*"}})
    assert "errors" not in result
    assert result["data"]["users"]["page"]["items"] == [{"id": str(other_user.id)}]


@pytest.mark.asyncio
async def test_users_query_filters_emails(query_admin_api, user):
    result = await query_admin_api(FILTER_USERS_QUERY, {"filters": {"email": "user@*"}})
    assert "errors" not in result
    assert result["data"]["users"]["page"]["items"] == [{"id": str(user.id)}]


@pytest.mark.asyncio
async def test_users_query_filters_admins(query_admin_api, admin, user):
    result = await query_admin_api(
        FILTER_USERS_QUERY, {"filters": {"isAdministrator": True}}
    )
    assert "errors" not in result
    assert result["data"]["users"]["page"]["items"] == [{"id": str(admin.id)}]


@pytest.mark.asyncio
async def test_users_query_filters_non_admins(query_admin_api, admin, user):
    result = await query_admin_api(
        FILTER_USERS_QUERY, {"filters": {"isAdministrator": False}}
    )
    assert "errors" not in result
    assert result["data"]["users"]["page"]["items"] == [{"id": str(user.id)}]


@pytest.mark.asyncio
async def test_users_query_filters_mods(query_admin_api, moderator, user):
    result = await query_admin_api(
        FILTER_USERS_QUERY, {"filters": {"isModerator": True}}
    )
    assert "errors" not in result
    assert result["data"]["users"]["page"]["items"] == [{"id": str(moderator.id)}]


@pytest.mark.asyncio
async def test_users_query_filters_non_mods(query_admin_api, admin, moderator):
    result = await query_admin_api(
        FILTER_USERS_QUERY, {"filters": {"isModerator": False}}
    )
    assert "errors" not in result
    assert result["data"]["users"]["page"]["items"] == [{"id": str(admin.id)}]


@pytest.mark.asyncio
async def test_users_query_filters_active_users(query_admin_api, admin, inactive_user):
    result = await query_admin_api(FILTER_USERS_QUERY, {"filters": {"isActive": True}})
    assert "errors" not in result
    assert result["data"]["users"]["page"]["items"] == [{"id": str(admin.id)}]


@pytest.mark.asyncio
async def test_users_query_filters_inactive_users(
    query_admin_api, admin, inactive_user
):
    result = await query_admin_api(FILTER_USERS_QUERY, {"filters": {"isActive": False}})
    assert "errors" not in result
    assert result["data"]["users"]["page"]["items"] == [{"id": str(inactive_user.id)}]
