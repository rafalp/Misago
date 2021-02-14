import pytest

from .....auth import get_user_from_token
from .....errors import ErrorsList
from ..login import resolve_login


@pytest.mark.asyncio
async def test_login_mutation_returns_user_token_on_success(
    graphql_info, user, user_password
):
    data = await resolve_login(
        None, graphql_info, username=user.name, password=user_password,
    )

    assert not data.get("errors")
    assert data.get("token")

    token_user = await get_user_from_token(graphql_info.context, data["token"])
    assert token_user == user


@pytest.mark.asyncio
async def test_login_mutation_returns_user_on_success(
    graphql_info, user, user_password
):
    data = await resolve_login(
        None, graphql_info, username=user.name, password=user_password,
    )

    assert not data.get("errors")
    assert data.get("user")
    assert data["user"] == user


@pytest.mark.asyncio
async def test_login_mutation_requires_username(graphql_info, user, user_password):
    data = await resolve_login(None, graphql_info, username="", password=user_password,)

    assert not data.get("user")
    assert not data.get("token")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == [ErrorsList.ROOT_LOCATION]
    assert data["errors"].get_errors_types() == ["value_error.all_fields_are_required"]


@pytest.mark.asyncio
async def test_login_mutation_requires_password(graphql_info, user, user_password):
    data = await resolve_login(None, graphql_info, username=user.name, password="",)

    assert not data.get("user")
    assert not data.get("token")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == [ErrorsList.ROOT_LOCATION]
    assert data["errors"].get_errors_types() == ["value_error.all_fields_are_required"]


@pytest.mark.asyncio
async def test_login_mutation_returns_error_on_nonexistent_user_credentials(
    graphql_info, user
):
    data = await resolve_login(
        None, graphql_info, username=user.name, password="invalid",
    )

    assert not data.get("user")
    assert not data.get("token")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == [ErrorsList.ROOT_LOCATION]
    assert data["errors"].get_errors_types() == ["value_error.invalid_credentials"]
