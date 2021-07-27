import pytest

from .....users.models import User


USER_CREATE_MUTATION = """
    mutation UserCreate($input: UserCreateInput) {
        userCreate(input: $input) {
            errors {
                location
                type
            }
            user {
                id
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_user_create_mutation_creates_user(query_admin_api):
    variables = {
        "input": {
            "name": "TestUser",
            "email": "test@example.com",
            "password": "password123",
        }
    }
    result = await query_admin_api(USER_CREATE_MUTATION, variables)

    data = result["data"]["userCreate"]
    assert not data["errors"]
    assert data["user"]["id"]

    user = await User.query.one(id=int(data["user"]["id"]))
    assert user.name == "TestUser"
    assert user.slug == "testuser"
    assert user.email == "test@example.com"
    assert await user.check_password("password123")


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_username_is_empty(
    query_admin_api,
):
    variables = {
        "input": {"name": " ", "email": "test@example.com", "password": "password123"}
    }
    result = await query_admin_api(USER_CREATE_MUTATION, variables)

    data = result["data"]["userCreate"]
    assert not data["user"]
    assert data["errors"] == [
        {"location": ["name"], "type": "value_error.any_str.min_length"}
    ]


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_username_is_invalid(
    query_admin_api,
):
    variables = {
        "input": {"name": "!!!", "email": "test@example.com", "password": "password123"}
    }
    result = await query_admin_api(USER_CREATE_MUTATION, variables)

    data = result["data"]["userCreate"]
    assert not data["user"]
    assert data["errors"] == [{"location": ["name"], "type": "value_error.username"}]


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_name_is_not_available(
    query_admin_api, user
):
    variables = {
        "input": {
            "name": user.name,
            "email": "test@example.com",
            "password": "password123",
        }
    }
    result = await query_admin_api(USER_CREATE_MUTATION, variables)

    data = result["data"]["userCreate"]
    assert not data["user"]
    assert data["errors"] == [
        {"location": ["name"], "type": "value_error.username.not_available"}
    ]


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_email_is_empty(
    query_admin_api, user
):
    variables = {
        "input": {"name": "NewUser", "email": "invalid.com", "password": "password123"}
    }
    result = await query_admin_api(USER_CREATE_MUTATION, variables)

    data = result["data"]["userCreate"]
    assert not data["user"]
    assert data["errors"] == [{"location": ["email"], "type": "value_error.email"}]


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_email_is_invalid(
    query_admin_api, user
):
    variables = {
        "input": {"name": "NewUser", "email": "invalid.com", "password": "password123"}
    }
    result = await query_admin_api(USER_CREATE_MUTATION, variables)

    data = result["data"]["userCreate"]
    assert not data["user"]
    assert data["errors"] == [{"location": ["email"], "type": "value_error.email"}]


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_email_is_not_available(
    query_admin_api, user
):
    variables = {
        "input": {"name": "NewUser", "email": user.email, "password": "password123"}
    }
    result = await query_admin_api(USER_CREATE_MUTATION, variables)

    data = result["data"]["userCreate"]
    assert not data["user"]
    assert data["errors"] == [
        {"location": ["email"], "type": "value_error.email.not_available"}
    ]


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_password_is_empty(
    query_admin_api,
):
    variables = {
        "input": {"name": "TestUser", "email": "test@example.com", "password": ""}
    }
    result = await query_admin_api(USER_CREATE_MUTATION, variables)

    data = result["data"]["userCreate"]
    assert not data["user"]
    assert data["errors"] == [
        {"location": ["password"], "type": "value_error.any_str.min_length"}
    ]


@pytest.mark.asyncio
async def test_user_create_mutation_returns_error_if_password_is_invalid(
    query_admin_api,
):
    variables = {
        "input": {"name": "TestUser", "email": "test@example.com", "password": "a"}
    }
    result = await query_admin_api(USER_CREATE_MUTATION, variables)

    data = result["data"]["userCreate"]
    assert not data["user"]
    assert data["errors"] == [
        {"location": ["password"], "type": "value_error.any_str.min_length"}
    ]
