from unittest.mock import ANY

import pytest

from .....users.models import User

USER_CREATE_MUTATION = """
    mutation UserCreate($input: UserCreateInput!) {
        userCreate(input: $input) {
            user {
                id
                name
                slug
                email
            }
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_user_create_mutation_creates_user(query_admin_api):
    result = await query_admin_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "TestUser",
                "email": "test@example.com",
                "password": "password123",
            },
        },
    )

    data = result["data"]["userCreate"]

    assert data == {
        "user": {
            "id": ANY,
            "name": "TestUser",
            "slug": "testuser",
            "email": "test@example.com",
        },
        "errors": None,
    }

    user = await User.query.one(id=int(data["user"]["id"]))
    assert user.name == "TestUser"
    assert user.slug == "testuser"
    assert user.email == "test@example.com"
    assert await user.check_password("password123")


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_username_is_empty(
    query_admin_api,
):
    result = await query_admin_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": " ",
                "email": "test@example.com",
                "password": "password123",
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "errors": [
            {
                "location": "name",
                "type": "value_error.any_str.min_length",
            },
        ],
    }


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_username_is_invalid(
    query_admin_api,
):
    result = await query_admin_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "!!!",
                "email": "test@example.com",
                "password": "password123",
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "errors": [
            {
                "location": "name",
                "type": "value_error.username",
            },
        ],
    }


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_name_is_not_available(
    query_admin_api, user
):
    result = await query_admin_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": user.name,
                "email": "test@example.com",
                "password": "password123",
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "errors": [
            {
                "location": "name",
                "type": "value_error.username.not_available",
            },
        ],
    }


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_email_is_empty(query_admin_api):
    result = await query_admin_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "NewUser",
                "email": "   ",
                "password": "password123",
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "errors": [
            {
                "location": "email",
                "type": "value_error.email",
            },
        ],
    }


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_email_is_invalid(query_admin_api):
    result = await query_admin_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "NewUser",
                "email": "invalid.com",
                "password": "password123",
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "errors": [
            {
                "location": "email",
                "type": "value_error.email",
            },
        ],
    }


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_email_is_not_available(
    query_admin_api, user
):
    result = await query_admin_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "NewUser",
                "email": user.email,
                "password": "password123",
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "errors": [
            {
                "location": "email",
                "type": "value_error.email.not_available",
            },
        ],
    }


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_password_is_empty(
    query_admin_api,
):
    result = await query_admin_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "TestUser",
                "email": "test@example.com",
                "password": "",
            }
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "errors": [
            {
                "location": "password",
                "type": "value_error.any_str.min_length",
            },
        ],
    }


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_password_is_too_long(
    query_admin_api,
):
    result = await query_admin_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "TestUser",
                "email": "test@example.com",
                "password": "a" * 256,
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "errors": [
            {
                "location": "password",
                "type": "value_error.any_str.max_length",
            },
        ],
    }


@pytest.mark.asyncio
async def test_user_create_mutation_requires_admin_auth(query_admin_api):
    result = await query_admin_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "TestUser",
                "email": "test@example.com",
                "password": "password123",
            },
        },
        include_auth=False,
        expect_error=True,
    )

    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None
