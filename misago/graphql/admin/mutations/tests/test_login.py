from unittest.mock import ANY

import pytest

from .....auth import get_user_from_token
from .....validation import ErrorsList

ADMIN_LOGIN_MUTATION = """
    mutation AdminLogin($username: String!, $password: String!) {
        login(username: $username, password: $password) {
            user {
                id
            }
            token
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_admin_login_mutation_returns_admin_user_and_token_on_success(
    query_admin_api, admin_graphql_info, admin, user_password
):
    result = await query_admin_api(
        ADMIN_LOGIN_MUTATION,
        {
            "username": admin.name,
            "password": user_password,
        },
        include_auth=False,
    )

    data = result["data"]["login"]

    assert data == {
        "user": {
            "id": str(admin.id),
        },
        "token": ANY,
        "errors": None,
    }

    token_user = await get_user_from_token(admin_graphql_info.context, data["token"])
    assert token_user == admin


@pytest.mark.asyncio
async def test_admin_login_mutation_requires_username(
    query_admin_api, user, user_password
):
    result = await query_admin_api(
        ADMIN_LOGIN_MUTATION,
        {
            "username": "",
            "password": user_password,
        },
        include_auth=False,
    )

    assert result["data"]["login"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": ErrorsList.ROOT_LOCATION,
                "type": "value_error.all_fields_are_required",
            },
        ],
    }


@pytest.mark.asyncio
async def test_admin_login_mutation_requires_password(query_admin_api, user):
    result = await query_admin_api(
        ADMIN_LOGIN_MUTATION,
        {
            "username": user.name,
            "password": "",
        },
        include_auth=False,
    )

    assert result["data"]["login"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": ErrorsList.ROOT_LOCATION,
                "type": "value_error.all_fields_are_required",
            },
        ],
    }


@pytest.mark.asyncio
async def test_admin_login_mutation_returns_error_on_nonexistant_user_credentials(
    query_admin_api, user
):
    result = await query_admin_api(
        ADMIN_LOGIN_MUTATION,
        {
            "username": user.name,
            "password": "invalid",
        },
        include_auth=False,
    )

    assert result["data"]["login"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": ErrorsList.ROOT_LOCATION,
                "type": "auth_error.invalid_credentials",
            },
        ],
    }


@pytest.mark.asyncio
async def test_admin_login_mutation_returns_error_if_user_is_not_admin(
    query_admin_api, user, user_password
):
    result = await query_admin_api(
        ADMIN_LOGIN_MUTATION,
        {
            "username": user.name,
            "password": user_password,
        },
        include_auth=False,
    )

    assert result["data"]["login"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": ErrorsList.ROOT_LOCATION,
                "type": "auth_error.not_admin",
            }
        ],
    }
