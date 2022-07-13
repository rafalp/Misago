import pytest

USER_GROUP_QUERY = """
    query GetUserGroup($id: ID!) {
        userGroup(id: $id) {
            id
            name
        }
    }
"""


@pytest.mark.asyncio
async def test_user_group_query_is_resolved_by_id(query_public_api, admins):
    result = await query_public_api(USER_GROUP_QUERY, {"id": str(admins.id)})
    assert result["data"]["userGroup"] == {
        "id": str(admins.id),
        "name": admins.name,
    }


@pytest.mark.asyncio
async def test_user_group_query_is_resolved_to_none_for_nonexisting_group(
    query_public_api, admins
):
    result = await query_public_api(USER_GROUP_QUERY, {"id": str(admins.id * 1000)})
    assert result["data"]["userGroup"] is None


@pytest.mark.asyncio
async def test_user_group_query_is_resolved_to_none_for_invalid_id(
    query_public_api, members
):
    result = await query_public_api(USER_GROUP_QUERY, {"id": "invalid"})
    assert result["data"]["userGroup"] is None


@pytest.mark.asyncio
async def test_user_group_query_is_resolved_to_none_for_hidden_group(
    query_public_api, guests
):
    result = await query_public_api(USER_GROUP_QUERY, {"id": str(guests.id)})
    assert result["data"]["userGroup"] is None


@pytest.mark.asyncio
async def test_admin_schema_user_group_query_is_resolved_by_id(query_admin_api, admins):
    result = await query_admin_api(USER_GROUP_QUERY, {"id": str(admins.id)})
    assert result["data"]["userGroup"] == {
        "id": str(admins.id),
        "name": admins.name,
    }


@pytest.mark.asyncio
async def test_admin_schema_user_group_query_is_resolved_to_none_for_nonexisting_group(
    query_admin_api, members
):
    result = await query_admin_api(USER_GROUP_QUERY, {"id": str(members.id * 1000)})
    assert result["data"]["userGroup"] is None


@pytest.mark.asyncio
async def test_admin_schema_user_group_query_is_resolved_to_none_for_invalid_id(
    query_admin_api, members
):
    result = await query_admin_api(USER_GROUP_QUERY, {"id": "invalid"})
    assert result["data"]["userGroup"] is None


@pytest.mark.asyncio
async def test_admin_schema_user_group_query_returns_hidden_group(
    query_admin_api, guests
):
    result = await query_admin_api(USER_GROUP_QUERY, {"id": str(guests.id)})
    assert result["data"]["userGroup"] == {
        "id": str(guests.id),
        "name": guests.name,
    }


@pytest.mark.asyncio
async def test_admin_schema_user_group_query_requires_admin_auth(
    query_admin_api, admins
):
    result = await query_admin_api(
        USER_GROUP_QUERY, {"id": admins.id}, expect_error=True, include_auth=False
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"]["userGroup"] is None


USER_GROUPS_QUERY = """
    query UserGroups {
        userGroups {
            id
            name
        }
    }
"""


@pytest.mark.asyncio
async def test_user_groups_query_returns_list_of_visible_user_groups(
    query_public_api, admins, moderators, members, guests
):
    result = await query_public_api(USER_GROUPS_QUERY)
    assert result["data"]["userGroups"] == [
        {
            "id": str(admins.id),
            "name": admins.name,
        },
        {
            "id": str(moderators.id),
            "name": moderators.name,
        },
    ]


@pytest.mark.asyncio
async def test_admin_schema_user_groups_query_returns_list_of_all_user_groups(
    query_admin_api, admins, moderators, members, guests
):
    result = await query_admin_api(USER_GROUPS_QUERY)
    assert result["data"]["userGroups"] == [
        {
            "id": str(admins.id),
            "name": admins.name,
        },
        {
            "id": str(moderators.id),
            "name": moderators.name,
        },
        {
            "id": str(members.id),
            "name": members.name,
        },
        {
            "id": str(guests.id),
            "name": guests.name,
        },
    ]


@pytest.mark.asyncio
async def test_admin_schema_user_groups_query_requires_admin_auth(
    query_admin_api, admins
):
    result = await query_admin_api(
        USER_GROUPS_QUERY, expect_error=True, include_auth=False
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"]["userGroups"] is None


USER_GROUP_ADMIN_FIELDS_QUERY = """
    query UserGroup($id: ID!) {
        userGroup(id: $id) {
            id
            isDefault
            isGuest
            isHidden
            isModerator
            isAdmin
        }
    }
"""


@pytest.mark.asyncio
async def test_admin_schema_user_group_fields_query(
    query_admin_api, admins, members, guests
):
    result = await query_admin_api(USER_GROUP_ADMIN_FIELDS_QUERY, {"id": admins.id})
    assert result["data"]["userGroup"] == {
        "id": str(admins.id),
        "isDefault": False,
        "isGuest": False,
        "isHidden": False,
        "isModerator": True,
        "isAdmin": True,
    }

    result = await query_admin_api(USER_GROUP_ADMIN_FIELDS_QUERY, {"id": members.id})
    assert result["data"]["userGroup"] == {
        "id": str(members.id),
        "isDefault": True,
        "isGuest": False,
        "isHidden": True,
        "isModerator": False,
        "isAdmin": False,
    }

    result = await query_admin_api(USER_GROUP_ADMIN_FIELDS_QUERY, {"id": guests.id})
    assert result["data"]["userGroup"] == {
        "id": str(guests.id),
        "isDefault": False,
        "isGuest": True,
        "isHidden": True,
        "isModerator": False,
        "isAdmin": False,
    }
