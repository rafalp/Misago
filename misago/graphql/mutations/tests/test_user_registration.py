import pytest

from ....passwords import verify_password
from ....testing import override_dynamic_settings
from ....users.get import get_user_by_id
from ..register import resolve_register


@pytest.mark.asyncio
async def test_registration_mutation_creates_new_user_account(graphql_info):
    data = await resolve_register(
        None,
        graphql_info,
        input={
            "name": "John",
            "email": "john@example.com",
            "password": " password123 ",
        },
    )

    assert "errors" not in data
    assert "user" in data
    assert await get_user_by_id(data["user"]["id"])


@pytest.mark.asyncio
async def test_registration_mutation_preserves_spaces_in_user_password(graphql_info):
    data = await resolve_register(
        None,
        graphql_info,
        input={
            "name": "John",
            "email": "john@example.com",
            "password": " password123 ",
        },
    )

    assert "user" in data

    user = await get_user_by_id(data["user"]["id"])
    assert await verify_password(" password123 ", user["password"])


@pytest.mark.asyncio
@override_dynamic_settings(password_min_length=10)
async def test_registration_mutation_validates_min_password_length(graphql_info):
    data = await resolve_register(
        None,
        graphql_info,
        input={"name": "abcd", "email": "john@example.com", "password": "pass",},
    )

    assert "errors" in data
    assert data["errors"].get_errors_locations() == ["password"]
    assert data["errors"].get_errors_types() == ["value_error.any_str.min_length"]


@pytest.mark.asyncio
async def test_registration_mutation_validates_max_password_length(graphql_info):
    data = await resolve_register(
        None,
        graphql_info,
        input={"name": "abcd", "email": "john@example.com", "password": "p" * 60,},
    )

    assert "errors" in data
    assert data["errors"].get_errors_locations() == ["password"]
    assert data["errors"].get_errors_types() == ["value_error.any_str.max_length"]


@pytest.mark.asyncio
@override_dynamic_settings(username_min_length=10)
async def test_registration_mutation_validates_min_user_name_length(graphql_info):
    data = await resolve_register(
        None,
        graphql_info,
        input={
            "name": "abcd",
            "email": "john@example.com",
            "password": " password123 ",
        },
    )

    assert "errors" in data
    assert data["errors"].get_errors_locations() == ["name"]
    assert data["errors"].get_errors_types() == ["value_error.any_str.min_length"]


@pytest.mark.asyncio
@override_dynamic_settings(username_min_length=1, username_max_length=3)
async def test_registration_mutation_validates_max_user_name_length(graphql_info):
    data = await resolve_register(
        None,
        graphql_info,
        input={
            "name": "abcd",
            "email": "john@example.com",
            "password": " password123 ",
        },
    )

    assert "errors" in data
    assert data["errors"].get_errors_locations() == ["name"]
    assert data["errors"].get_errors_types() == ["value_error.any_str.max_length"]


@pytest.mark.asyncio
async def test_registration_mutation_validates_user_name_content(graphql_info):
    data = await resolve_register(
        None,
        graphql_info,
        input={
            "name": "invalid!",
            "email": "john@example.com",
            "password": " password123 ",
        },
    )

    assert "errors" in data
    assert data["errors"].get_errors_locations() == ["name"]
    assert data["errors"].get_errors_types() == ["value_error.username"]


@pytest.mark.asyncio
async def test_registration_mutation_validates_if_username_is_available(
    graphql_info, user
):
    data = await resolve_register(
        None,
        graphql_info,
        input={
            "name": user["name"],
            "email": "john@example.com",
            "password": " password123 ",
        },
    )

    assert "errors" in data
    assert data["errors"].get_errors_locations() == ["name"]
    assert data["errors"].get_errors_types() == ["value_error.username.not_available"]


@pytest.mark.asyncio
async def test_registration_mutation_validates_user_email(graphql_info):
    data = await resolve_register(
        None,
        graphql_info,
        input={"name": "John", "email": "invalidemail", "password": " password123 ",},
    )

    assert "errors" in data
    assert data["errors"].get_errors_locations() == ["email"]
    assert data["errors"].get_errors_types() == ["value_error.email"]


@pytest.mark.asyncio
async def test_registration_mutation_validates_if_user_email_is_available(
    graphql_info, user
):
    data = await resolve_register(
        None,
        graphql_info,
        input={"name": "John", "email": user["email"], "password": " password123 ",},
    )

    assert "errors" in data
    assert data["errors"].get_errors_locations() == ["email"]
    assert data["errors"].get_errors_types() == ["value_error.email.not_available"]
