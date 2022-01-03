from unittest.mock import ANY

import pytest

from .....auth import get_user_from_token
from .....errors import ErrorsList

LOGIN_MUTATION = """
    mutation Login($username: String!, $password: String!) {
        login(username: $username, password: $password) {
            user {
                id
                name
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
async def test_login_mutation_returns_user_and_token_on_success(
    graphql_info, query_public_api, user, user_password
):
    result = await query_public_api(
        LOGIN_MUTATION,
        {"username": user.name, "password": user_password},
    )

    assert result["data"]["login"] == {
        "user": {
            "id": str(user.id),
            "name": user.name,
        },
        "token": ANY,
        "errors": None,
    }

    token_user = await get_user_from_token(
        graphql_info.context, result["data"]["login"]["token"]
    )
    assert token_user == user


@pytest.mark.asyncio
async def test_login_mutation_requires_username(query_public_api, user, user_password):
    result = await query_public_api(
        LOGIN_MUTATION,
        {"username": "", "password": user_password},
    )

    assert result["data"]["login"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": [ErrorsList.ROOT_LOCATION],
                "type": "value_error.all_fields_are_required",
            },
        ],
    }


@pytest.mark.asyncio
async def test_login_mutation_requires_password(query_public_api, user):
    result = await query_public_api(
        LOGIN_MUTATION,
        {"username": user.name, "password": ""},
    )

    assert result["data"]["login"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": [ErrorsList.ROOT_LOCATION],
                "type": "value_error.all_fields_are_required",
            },
        ],
    }


@pytest.mark.asyncio
async def test_login_mutation_returns_error_on_nonexistent_user_credentials(
    query_public_api, db
):
    result = await query_public_api(
        LOGIN_MUTATION,
        {"username": "John", "password": "secret123"},
    )

    assert result["data"]["login"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": [ErrorsList.ROOT_LOCATION],
                "type": "value_error.invalid_credentials",
            },
        ],
    }
