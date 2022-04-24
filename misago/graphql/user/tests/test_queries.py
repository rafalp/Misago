import pytest

USER_QUERY = """
    query GetUser($user: ID!) {
        user(id: $user) {
            id
            name
        }
    }
"""


@pytest.mark.asyncio
async def test_user_query_is_resolved_by_id(query_public_api, user):
    result = await query_public_api(USER_QUERY, {"user": str(user.id)})
    assert result["data"]["user"] == {
        "id": str(user.id),
        "name": user.name,
    }


@pytest.mark.asyncio
async def test_user_query_is_resolved_to_none_for_nonexisting_user(
    query_public_api, user
):
    result = await query_public_api(USER_QUERY, {"user": str(user.id * 1000)})
    assert result["data"]["user"] is None


@pytest.mark.asyncio
async def test_user_query_is_resolved_to_none_for_invalid_id(query_public_api, user):
    result = await query_public_api(USER_QUERY, {"user": "invalid"})
    assert result["data"]["user"] is None


@pytest.mark.asyncio
async def test_user_query_is_resolved_to_none_for_inactive_user(query_public_api, user):
    await user.update(is_active=False)
    result = await query_public_api(USER_QUERY, {"user": str(user.id)})
    assert result["data"]["user"] is None


@pytest.mark.asyncio
async def test_admin_schema_user_query_is_resolved_by_id(query_admin_api, user):
    result = await query_admin_api(USER_QUERY, {"user": str(user.id)})
    assert result["data"]["user"] == {
        "id": str(user.id),
        "name": user.name,
    }


@pytest.mark.asyncio
async def test_admin_schema_user_query_is_resolved_to_none_for_nonexisting_user(
    query_admin_api, user
):
    result = await query_admin_api(USER_QUERY, {"user": str(user.id * 1000)})
    assert result["data"]["user"] is None


@pytest.mark.asyncio
async def test_admin_schema_user_query_is_resolved_to_none_for_invalid_id(
    query_admin_api, user
):
    result = await query_admin_api(USER_QUERY, {"user": "invalid"})
    assert result["data"]["user"] is None


@pytest.mark.asyncio
async def test_admin_schema_user_query_is_resolved_to_inactive_user(
    query_admin_api, user
):
    await user.update(is_active=False)
    result = await query_admin_api(USER_QUERY, {"user": str(user.id)})
    assert result["data"]["user"] == {
        "id": str(user.id),
        "name": user.name,
    }


@pytest.mark.asyncio
async def test_admin_schema_user_query_requires_admin_auth(query_admin_api, admin):
    result = await query_admin_api(
        USER_QUERY, {"user": admin.id}, expect_error=True, include_auth=False
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"]["user"] is None


USERS_QUERY = """
    query Users($filters: UsersFilters, $page: Int) {
        users(filters: $filters, page: $page) {
            totalCount
            totalPages
            results {
                id
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_admin_schema_users_query_returns_first_page_of_users_list(
    query_admin_api, admin
):
    result = await query_admin_api(USERS_QUERY)

    assert result["data"]["users"] == {
        "totalCount": 1,
        "totalPages": 1,
        "results": [
            {
                "id": str(admin.id),
            },
        ],
    }


@pytest.mark.asyncio
async def test_admin_schema_users_query_filters_names(query_admin_api, other_user):
    result = await query_admin_api(USERS_QUERY, {"filters": {"name": "Other*"}})
    assert result["data"]["users"]["results"] == [{"id": str(other_user.id)}]


@pytest.mark.asyncio
async def test_admin_schema_users_query_filters_emails(query_admin_api, user):
    result = await query_admin_api(USERS_QUERY, {"filters": {"email": "user@*"}})
    assert result["data"]["users"]["results"] == [{"id": str(user.id)}]


@pytest.mark.asyncio
async def test_admin_schema_users_query_filters_admins(query_admin_api, admin, user):
    result = await query_admin_api(USERS_QUERY, {"filters": {"isAdmin": True}})
    assert result["data"]["users"]["results"] == [{"id": str(admin.id)}]


@pytest.mark.asyncio
async def test_admin_schema_users_query_filters_non_admins(
    query_admin_api, admin, user
):
    result = await query_admin_api(USERS_QUERY, {"filters": {"isAdmin": False}})
    assert result["data"]["users"]["results"] == [{"id": str(user.id)}]


@pytest.mark.asyncio
async def test_admin_schema_users_query_filters_mods(query_admin_api, moderator, user):
    result = await query_admin_api(USERS_QUERY, {"filters": {"isModerator": True}})
    assert result["data"]["users"]["results"] == [{"id": str(moderator.id)}]


@pytest.mark.asyncio
async def test_admin_schema_users_query_filters_non_mods(
    query_admin_api, admin, moderator
):
    result = await query_admin_api(USERS_QUERY, {"filters": {"isModerator": False}})
    assert result["data"]["users"]["results"] == [{"id": str(admin.id)}]


@pytest.mark.asyncio
async def test_admin_schema_users_query_filters_active_users(
    query_admin_api, admin, inactive_user
):
    result = await query_admin_api(USERS_QUERY, {"filters": {"isActive": True}})
    assert result["data"]["users"]["results"] == [{"id": str(admin.id)}]


@pytest.mark.asyncio
async def test_admin_schema_users_query_filters_inactive_users(
    query_admin_api, admin, inactive_user
):
    result = await query_admin_api(USERS_QUERY, {"filters": {"isActive": False}})
    assert result["data"]["users"]["results"] == [{"id": str(inactive_user.id)}]


@pytest.mark.asyncio
async def test_admin_schema_users_query_requires_admin_auth(query_admin_api):
    result = await query_admin_api(
        USERS_QUERY,
        {"filters": {"isActive": False}},
        expect_error=True,
        include_auth=False,
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"]["users"] is None
