import pytest

from .....users.models import User

USER_UPDATE_MUTATION = """
    mutation UserUpdate($id: ID!, $input: UserUpdateInput!) {
        userUpdate(user: $id, input: $input) {
            updated
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
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_id_is_invalid(query_admin_api):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": "invalid",
            "input": {},
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["user"]
    assert data["errors"] == [
        {
            "location": ["user"],
            "type": "type_error.integer",
        },
    ]


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_doesnt_exist(query_admin_api, admin):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(admin.id + 1),
            "input": {},
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["user"]
    assert data["errors"] == [
        {
            "location": ["user"],
            "type": "value_error.user.not_exists",
        },
    ]


@pytest.mark.asyncio
async def test_user_update_mutation_updates_user_name(query_admin_api, user):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "name": "UpdatedUser",
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert data["user"]["name"] == "UpdatedUser"
    assert data["user"]["slug"] == "updateduser"

    user_from_db = await user.refresh_from_db()
    assert user_from_db.name == "UpdatedUser"
    assert user_from_db.slug == "updateduser"


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_name_is_invalid(
    query_admin_api, user
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "name": "!!!!",
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {
            "location": ["name"],
            "type": "value_error.username",
        },
    ]
    assert data["user"]["name"] == user.name
    assert data["user"]["slug"] == user.slug

    user_from_db = await user.refresh_from_db()
    assert user_from_db.name == user.name
    assert user_from_db.slug == user.slug


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_name_is_not_available(
    query_admin_api, user
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "name": "Admin",
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {
            "location": ["name"],
            "type": "value_error.username.not_available",
        },
    ]
    assert data["user"]["name"] == user.name
    assert data["user"]["slug"] == user.slug

    user_from_db = await user.refresh_from_db()
    assert user_from_db.name == user.name
    assert user_from_db.slug == user.slug


@pytest.mark.asyncio
async def test_user_update_mutation_skips_update_if_new_name_is_same(
    query_admin_api, user
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "name": "User",
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert data["user"]["name"] == user.name
    assert data["user"]["slug"] == user.slug

    user_from_db = await user.refresh_from_db()
    assert user_from_db.name == user.name
    assert user_from_db.slug == user.slug


@pytest.mark.asyncio
async def test_user_update_mutation_updates_user_email(query_admin_api, user):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "email": "new@email.com",
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert data["user"]["email"] == "new@email.com"

    user_from_db = await user.refresh_from_db()
    assert user_from_db.email == "new@email.com"


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_email_is_invalid(
    query_admin_api, user
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "email": "invalid",
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {
            "location": ["email"],
            "type": "value_error.email",
        },
    ]
    assert data["user"]["email"] == user.email

    user_from_db = await user.refresh_from_db()
    assert user_from_db.email == user.email


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_email_is_not_available(
    query_admin_api, admin, user
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "email": admin.email,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {
            "location": ["email"],
            "type": "value_error.email.not_available",
        },
    ]
    assert data["user"]["email"] == user.email

    user_from_db = await user.refresh_from_db()
    assert user_from_db.email == user.email


@pytest.mark.asyncio
async def test_user_update_mutation_skips_update_if_new_email_is_same(
    query_admin_api, user
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "email": user.email,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert data["user"]["email"] == user.email

    user_from_db = await user.refresh_from_db()
    assert user_from_db.email == user.email


@pytest.mark.asyncio
async def test_user_update_mutation_updates_user_password(query_admin_api, user):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "password": "n3wp5ssword  ",
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]

    user_from_db = await user.refresh_from_db()
    assert await user_from_db.check_password("n3wp5ssword  ")


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_password_is_invalid(
    query_admin_api, user, user_password
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "password": "a",
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {
            "location": ["password"],
            "type": "value_error.any_str.min_length",
        },
    ]

    user_from_db = await user.refresh_from_db()
    assert await user_from_db.check_password(user_password)


@pytest.mark.asyncio
async def test_user_update_mutation_updates_user_full_name(query_admin_api, user):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "fullName": "Bob Bobertson",
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert data["user"]["fullName"] == "Bob Bobertson"

    user_from_db = await user.refresh_from_db()
    assert user_from_db.full_name == "Bob Bobertson"


@pytest.mark.asyncio
async def test_user_update_mutation_clears_user_full_name(query_admin_api, user):
    user = await user.update(full_name="Bob Bobertson")

    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "fullName": "",
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert data["user"]["fullName"] is None

    user_from_db = await user.refresh_from_db()
    assert user_from_db.full_name is None


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_full_name_is_too_long(
    query_admin_api, user
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "fullName": "Bob Bobertson" * 20,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {
            "location": ["fullName"],
            "type": "value_error.any_str.max_length",
        },
    ]
    assert not data["user"]["fullName"]

    user_from_db = await user.refresh_from_db()
    assert not user_from_db.full_name


@pytest.mark.asyncio
async def test_user_update_mutation_skips_update_if_new_full_name_is_same(
    query_admin_api, user
):
    user = await user.update(full_name="Bob Bobertson")

    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "fullName": "Bob Bobertson",
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert not data["updated"]
    assert data["user"]["fullName"] == "Bob Bobertson"

    user_from_db = await user.refresh_from_db()
    assert user_from_db.full_name == "Bob Bobertson"


@pytest.mark.asyncio
async def test_user_update_mutation_updates_admin_status_to_true(query_admin_api, user):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isAdmin": True,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert data["user"]["isAdmin"]

    user_from_db = await user.refresh_from_db()
    assert user_from_db.is_admin


@pytest.mark.asyncio
async def test_user_update_mutation_updates_admin_status_to_false(
    query_admin_api, user
):
    user = await user.update(is_admin=True)

    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isAdmin": False,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert not data["user"]["isAdmin"]

    user_from_db = await user.refresh_from_db()
    assert not user_from_db.is_admin


@pytest.mark.asyncio
async def test_admin_update_mutation_skips_update_if_admin_status_is_same(
    query_admin_api, admin
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(admin.id),
            "input": {
                "isAdmin": True,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert data["user"]["isAdmin"]

    admin_from_db = await admin.refresh_from_db()
    assert admin_from_db.is_admin


@pytest.mark.asyncio
async def test_user_update_mutation_skips_update_if_admin_status_is_same(
    query_admin_api, user
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isAdmin": False,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert not data["user"]["isAdmin"]

    user_from_db = await user.refresh_from_db()
    assert not user_from_db.is_admin


@pytest.mark.asyncio
async def test_admin_update_mutation_fails_if_admin_tries_to_remove_own_status(
    query_admin_api, admin
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(admin.id),
            "input": {
                "isAdmin": False,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {
            "location": ["isAdmin"],
            "type": "value_error.user.remove_own_admin",
        },
    ]
    assert data["user"]["isAdmin"]

    admin_from_db = await admin.refresh_from_db()
    assert admin_from_db.is_admin


@pytest.mark.asyncio
async def test_user_update_mutation_updates_moderator_status_to_true(
    query_admin_api, user
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isModerator": True,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert data["user"]["isModerator"]

    user_from_db = await user.refresh_from_db()
    assert user_from_db.is_moderator


@pytest.mark.asyncio
async def test_user_update_mutation_updates_moderator_status_to_false(
    query_admin_api, moderator
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(moderator.id),
            "input": {
                "isModerator": False,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert not data["user"]["isModerator"]

    moderator_from_db = await moderator.refresh_from_db()
    assert not moderator_from_db.is_moderator


@pytest.mark.asyncio
async def test_moderator_update_mutation_skips_update_if_moderator_status_is_same(
    query_admin_api, moderator
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(moderator.id),
            "input": {
                "isModerator": True,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert data["user"]["isModerator"]

    moderator_from_db = await moderator.refresh_from_db()
    assert moderator_from_db.is_moderator


@pytest.mark.asyncio
async def test_user_update_mutation_skips_update_if_moderator_status_is_same(
    query_admin_api, user
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isModerator": False,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert not data["user"]["isModerator"]

    user_from_db = await user.refresh_from_db()
    assert not user_from_db.is_moderator


@pytest.mark.asyncio
async def test_inactive_user_update_mutation_updates_active_status_to_true(
    query_admin_api, inactive_user
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(inactive_user.id),
            "input": {
                "isActive": True,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert data["user"]["isActive"]

    inactive_user_from_db = await inactive_user.refresh_from_db()
    assert inactive_user_from_db.is_active


@pytest.mark.asyncio
async def test_user_update_mutation_updates_active_status_to_false(
    query_admin_api, user
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isActive": False,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["errors"]
    assert data["updated"]
    assert not data["user"]["isActive"]

    user_from_db = await user.refresh_from_db()
    assert not user_from_db.is_active


@pytest.mark.asyncio
async def test_user_update_mutation_fails_if_user_deactivates_themselves(
    query_admin_api, admin
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(admin.id),
            "input": {
                "isActive": False,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert data["errors"] == [
        {
            "location": ["isActive"],
            "type": "value_error.user.deactivate_self",
        },
    ]
    assert data["user"]["isActive"]

    admin_from_db = await admin.refresh_from_db()
    assert admin_from_db.is_active


@pytest.mark.asyncio
async def test_inactive_user_update_mutation_skips_update_if_active_status_is_same(
    query_admin_api, inactive_user
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(inactive_user.id),
            "input": {
                "isActive": False,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert not data["user"]["isActive"]

    inactive_user_from_db = await inactive_user.refresh_from_db()
    assert not inactive_user_from_db.is_active


@pytest.mark.asyncio
async def test_user_update_mutation_skips_update_if_active_status_is_same(
    query_admin_api, user
):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isActive": True,
            },
        },
    )

    data = result["data"]["userUpdate"]
    assert not data["updated"]
    assert not data["errors"]
    assert data["user"]["isActive"]

    user_from_db = await user.refresh_from_db()
    assert user_from_db.is_active


@pytest.mark.asyncio
async def test_user_update_mutation_requires_admin_auth(query_admin_api, user):
    result = await query_admin_api(
        USER_UPDATE_MUTATION,
        {
            "id": str(user.id),
            "input": {
                "isActive": True,
            },
        },
        include_auth=False,
        expect_error=True,
    )

    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None
