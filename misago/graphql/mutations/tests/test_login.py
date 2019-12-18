import pytest

from ....auth import get_user_from_token
from ..login import resolve_login


@pytest.mark.asyncio
async def test_login_mutation_returns_user_token_on_success(
    graphql_info, user, user_password
):
    data = await resolve_login(
        None, graphql_info, username=user.name, password=user_password,
    )

    assert "error" not in data
    assert "token" in data

    token_user = await get_user_from_token(graphql_info.context, data["token"])
    assert token_user == user


@pytest.mark.asyncio
async def test_login_mutation_returns_user_on_success(
    graphql_info, user, user_password
):
    data = await resolve_login(
        None, graphql_info, username=user.name, password=user_password,
    )

    assert "error" not in data
    assert "user" in data
    assert data["user"] == user


@pytest.mark.asyncio
async def test_login_mutation_requires_username(graphql_info, user, user_password):
    data = await resolve_login(None, graphql_info, username="", password=user_password,)

    assert "error" in data
    assert data["error"]["type"] == "value_error.all_fields_are_required"
    assert "user" not in data
    assert "token" not in data


@pytest.mark.asyncio
async def test_login_mutation_requires_password(graphql_info, user, user_password):
    data = await resolve_login(None, graphql_info, username=user.name, password="",)

    assert "error" in data
    assert data["error"]["type"] == "value_error.all_fields_are_required"
    assert "user" not in data
    assert "token" not in data


@pytest.mark.asyncio
async def test_login_mutation_returns_error_on_nonexistent_user_credentials(
    graphql_info, user
):
    data = await resolve_login(
        None, graphql_info, username=user.name, password="invalid",
    )

    assert "error" in data
    assert data["error"]["type"] == "value_error.invalid_credentials"
    assert "user" not in data
    assert "token" not in data
