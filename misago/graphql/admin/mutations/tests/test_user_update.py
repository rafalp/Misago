import pytest

from .....users.models import User

USER_UPDATE_MUTATION = """
    mutation UserUpdate($id: ID!, $input: UserUpdateInput!) {
        userUpdate(user: $id, input: $input) {
            updated
            errors {
                location
                type
            }
            user {
                id
                name
                slug
                fullName
                email
                isActive
                isAdmin
                isModerator
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_id_is_invalid(query_admin_api):
    variables = {"id": "invalid", "input": {}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["user"]
    assert data["errors"] == [{"location": ["user"], "type": "type_error.integer"}]


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_doesnt_exist(query_admin_api, admin):
    variables = {"id": str(admin.id + 1), "input": {}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["user"]
    assert data["errors"] == [
        {"location": ["user"], "type": "value_error.user.not_exists"}
    ]


@pytest.mark.asyncio
async def test_user_update_mutation_updates_user_name(query_admin_api, user):
    variables = {
        "id": str(user.id),
        "input": {
            "name": "UpdatedUser",
        },
    }
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert data["user"]["name"] == "UpdatedUser"
    assert data["user"]["slug"] == "updateduser"

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.name == "UpdatedUser"
    assert updated_user.slug == "updateduser"


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_name_is_invalid(
    query_admin_api, user
):
    variables = {
        "id": str(user.id),
        "input": {
            "name": "!!!!",
        },
    }
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [{"location": ["name"], "type": "value_error.username"}]
    assert data["user"]["name"] == user.name
    assert data["user"]["slug"] == user.slug

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.name == user.name
    assert updated_user.slug == user.slug


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_name_is_not_available(
    query_admin_api, user
):
    variables = {"id": str(user.id), "input": {"name": "Admin"}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {"location": ["name"], "type": "value_error.username.not_available"}
    ]
    assert data["user"]["name"] == user.name
    assert data["user"]["slug"] == user.slug

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.name == user.name
    assert updated_user.slug == user.slug


@pytest.mark.asyncio
async def test_user_update_mutation_skips_update_if_new_name_is_same(
    query_admin_api, user
):
    variables = {"id": str(user.id), "input": {"name": "User"}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert data["user"]["name"] == user.name
    assert data["user"]["slug"] == user.slug

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.name == user.name
    assert updated_user.slug == user.slug


@pytest.mark.asyncio
async def test_user_update_mutation_updates_user_email(query_admin_api, user):
    variables = {
        "id": str(user.id),
        "input": {
            "email": "new@email.com",
        },
    }
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert data["user"]["email"] == "new@email.com"

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.email == "new@email.com"


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_email_is_invalid(
    query_admin_api, user
):
    variables = {
        "id": str(user.id),
        "input": {
            "email": "invalid",
        },
    }
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [{"location": ["email"], "type": "value_error.email"}]
    assert data["user"]["email"] == user.email

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.email == user.email


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_email_is_not_available(
    query_admin_api, admin, user
):
    variables = {"id": str(user.id), "input": {"email": admin.email}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {"location": ["email"], "type": "value_error.email.not_available"}
    ]
    assert data["user"]["email"] == user.email

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.email == user.email


@pytest.mark.asyncio
async def test_user_update_mutation_skips_update_if_new_email_is_same(
    query_admin_api, user
):
    variables = {"id": str(user.id), "input": {"email": user.email}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert data["user"]["email"] == user.email

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.email == user.email


@pytest.mark.asyncio
async def test_user_update_mutation_updates_user_password(query_admin_api, user):
    variables = {
        "id": str(user.id),
        "input": {
            "password": "n3wp5ssword  ",
        },
    }
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert await updated_user.check_password("n3wp5ssword  ")


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_password_is_invalid(
    query_admin_api, user, user_password
):
    variables = {
        "id": str(user.id),
        "input": {
            "password": "a",
        },
    }
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {"location": ["password"], "type": "value_error.any_str.min_length"}
    ]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert await updated_user.check_password(user_password)


@pytest.mark.asyncio
async def test_user_update_mutation_updates_user_full_name(query_admin_api, user):
    variables = {
        "id": str(user.id),
        "input": {
            "fullName": "Bob Bobertson",
        },
    }
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert data["user"]["fullName"] == "Bob Bobertson"

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.full_name == "Bob Bobertson"


@pytest.mark.asyncio
async def test_user_update_mutation_clears_user_full_name(query_admin_api, user):
    user = await user.update(full_name="Bob Bobertson")
    variables = {
        "id": str(user.id),
        "input": {
            "fullName": "",
        },
    }
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert data["user"]["fullName"] is None

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.full_name is None


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_full_name_is_too_long(
    query_admin_api, user
):
    variables = {
        "id": str(user.id),
        "input": {
            "fullName": "Bob Bobertson" * 20,
        },
    }
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {"location": ["fullName"], "type": "value_error.any_str.max_length"}
    ]
    assert not data["user"]["fullName"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert not updated_user.full_name


@pytest.mark.asyncio
async def test_user_update_mutation_skips_update_if_new_full_name_is_same(
    query_admin_api, user
):
    user = await user.update(full_name="Bob Bobertson")
    variables = {
        "id": str(user.id),
        "input": {
            "fullName": "Bob Bobertson",
        },
    }
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert not data["updated"]
    assert data["user"]["fullName"] == "Bob Bobertson"

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.full_name == "Bob Bobertson"


@pytest.mark.asyncio
async def test_user_update_mutation_updates_admin_status_to_true(query_admin_api, user):
    variables = {"id": str(user.id), "input": {"isAdmin": True}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert data["user"]["isAdmin"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.is_admin


@pytest.mark.asyncio
async def test_user_update_mutation_updates_admin_status_to_false(
    query_admin_api, user
):
    user = await user.update(is_admin=True)

    variables = {"id": str(user.id), "input": {"isAdmin": False}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert not data["user"]["isAdmin"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert not updated_user.is_admin


@pytest.mark.asyncio
async def test_admin_update_mutation_skips_update_if_admin_status_is_same(
    query_admin_api, admin
):
    variables = {"id": str(admin.id), "input": {"isAdmin": True}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert data["user"]["isAdmin"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.is_admin


@pytest.mark.asyncio
async def test_user_update_mutation_skips_update_if_admin_status_is_same(
    query_admin_api, user
):
    variables = {"id": str(user.id), "input": {"isAdmin": False}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert not data["user"]["isAdmin"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert not updated_user.is_admin


@pytest.mark.asyncio
async def test_admin_update_mutation_fails_if_admin_tries_to_remove_own_status(
    query_admin_api, admin
):
    variables = {"id": str(admin.id), "input": {"isAdmin": False}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {"location": ["isAdmin"], "type": "value_error.user.remove_own_admin"}
    ]
    assert data["user"]["isAdmin"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.is_admin


@pytest.mark.asyncio
async def test_user_update_mutation_updates_moderator_status_to_true(
    query_admin_api, user
):
    variables = {"id": str(user.id), "input": {"isModerator": True}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert data["user"]["isModerator"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.is_moderator


@pytest.mark.asyncio
async def test_user_update_mutation_updates_moderator_status_to_false(
    query_admin_api, moderator
):
    variables = {"id": str(moderator.id), "input": {"isModerator": False}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert not data["user"]["isModerator"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert not updated_user.is_moderator


@pytest.mark.asyncio
async def test_moderator_update_mutation_skips_update_if_moderator_status_is_same(
    query_admin_api, moderator
):
    variables = {"id": str(moderator.id), "input": {"isModerator": True}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert data["user"]["isModerator"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.is_moderator


@pytest.mark.asyncio
async def test_user_update_mutation_skips_update_if_moderator_status_is_same(
    query_admin_api, user
):
    variables = {"id": str(user.id), "input": {"isModerator": False}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert not data["user"]["isModerator"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert not updated_user.is_moderator


@pytest.mark.asyncio
async def test_inactive_user_update_mutation_updates_active_status_to_true(
    query_admin_api, inactive_user
):
    variables = {"id": str(inactive_user.id), "input": {"isActive": True}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert data["user"]["isActive"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.is_active


@pytest.mark.asyncio
async def test_user_update_mutation_updates_active_status_to_false(
    query_admin_api, user
):
    variables = {"id": str(user.id), "input": {"isActive": False}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert not data["user"]["isActive"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert not updated_user.is_active


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_deastives_themselves(
    query_admin_api, admin
):
    variables = {"id": str(admin.id), "input": {"isActive": False}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {"location": ["isActive"], "type": "value_error.user.deactivate_self"}
    ]
    assert data["user"]["isActive"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.is_active


@pytest.mark.asyncio
async def test_inactive_user_update_mutation_skips_update_if_active_status_is_same(
    query_admin_api, inactive_user
):
    variables = {"id": str(inactive_user.id), "input": {"isActive": False}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert not data["user"]["isActive"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert not updated_user.is_active


@pytest.mark.asyncio
async def test_user_update_mutation_skips_update_if_active_status_is_same(
    query_admin_api, user
):
    variables = {"id": str(user.id), "input": {"isActive": True}}
    result = await query_admin_api(USER_UPDATE_MUTATION, variables)

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert data["user"]["isActive"]

    updated_user = await User.query.one(id=int(data["user"]["id"]))
    assert updated_user.is_active


@pytest.mark.asyncio
async def test_user_update_mutation_requires_admin_auth(query_admin_api, user):
    variables = {"id": str(user.id), "input": {"isActive": True}}
    result = await query_admin_api(
        USER_UPDATE_MUTATION, variables, include_auth=False, expect_error=True
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None
