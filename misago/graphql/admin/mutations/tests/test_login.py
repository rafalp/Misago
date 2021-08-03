import pytest

from .....auth import get_user_from_token
from .....errors import ErrorsList

ADMIN_LOGIN_MUTATION = """
    mutation AdminLogin($username: String!, $password: String!) {
        login(username: $username, password: $password) {
            errors {
                location
                type
            }
            user {
                id
            }
            token
        }
    }
"""


@pytest.mark.asyncio
async def test_admin_login_mutation_returns_admin_token_on_success(
    query_admin_api, admin_graphql_info, admin, user_password
):
    variables = {"username": admin.name, "password": user_password}
    result = await query_admin_api(ADMIN_LOGIN_MUTATION, variables, include_auth=False)
    data = result["data"]["login"]
    assert not data["errors"]
    assert data["token"]

    token_user = await get_user_from_token(admin_graphql_info.context, data["token"])
    assert token_user == admin


@pytest.mark.asyncio
async def test_admin_login_mutation_returns_admin_user_on_success(
    query_admin_api, admin, user_password
):
    variables = {"username": admin.name, "password": user_password}
    result = await query_admin_api(ADMIN_LOGIN_MUTATION, variables, include_auth=False)
    data = result["data"]["login"]
    assert not data["errors"]
    assert data["user"]

    assert not data.get("errors")
    assert data.get("user")
    assert data["user"]["id"] == str(admin.id)


@pytest.mark.asyncio
async def test_admin_login_mutation_requires_username(
    query_admin_api, user, user_password
):
    variables = {"username": "", "password": user_password}
    result = await query_admin_api(ADMIN_LOGIN_MUTATION, variables, include_auth=False)
    data = result["data"]["login"]
    assert not data["token"]
    assert not data["user"]
    assert data["errors"] == [
        {
            "location": [ErrorsList.ROOT_LOCATION],
            "type": "value_error.all_fields_are_required",
        }
    ]


@pytest.mark.asyncio
async def test_admin_login_mutation_requires_password(
    query_admin_api, user, user_password
):
    variables = {"username": user.name, "password": ""}
    result = await query_admin_api(ADMIN_LOGIN_MUTATION, variables, include_auth=False)
    data = result["data"]["login"]
    assert not data["token"]
    assert not data["user"]
    assert data["errors"] == [
        {
            "location": [ErrorsList.ROOT_LOCATION],
            "type": "value_error.all_fields_are_required",
        }
    ]


@pytest.mark.asyncio
async def test_admin_login_mutation_returns_error_on_nonexistent_user_credentials(
    query_admin_api, user
):
    variables = {"username": user.name, "password": "invalid"}
    result = await query_admin_api(ADMIN_LOGIN_MUTATION, variables, include_auth=False)
    data = result["data"]["login"]
    assert not data["token"]
    assert not data["user"]
    assert data["errors"] == [
        {
            "location": [ErrorsList.ROOT_LOCATION],
            "type": "value_error.invalid_credentials",
        }
    ]


@pytest.mark.asyncio
async def test_admin_login_mutation_returns_error_if_user_is_not_admin(
    query_admin_api, user, user_password
):
    variables = {"username": user.name, "password": user_password}
    result = await query_admin_api(ADMIN_LOGIN_MUTATION, variables, include_auth=False)
    data = result["data"]["login"]
    assert not data["token"]
    assert not data["user"]
    assert data["errors"] == [
        {"location": [ErrorsList.ROOT_LOCATION], "type": "auth_error.not_admin"}
    ]
