from unittest.mock import ANY

import pytest

from .....auth import get_user_from_token
from .....passwords import check_password
from .....testing import override_dynamic_settings
from .....users.models import User

USER_CREATE_MUTATION = """
    mutation UserCreate($input: UserCreateInput!) {
        userCreate(input: $input) {
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
async def test_user_create_mutation_creates_new_user_account(
    query_public_api, graphql_info, db
):
    result = await query_public_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "John",
                "email": "john@example.com",
                "password": " password123 ",
            },
        },
    )

    data = result["data"]["userCreate"]

    assert data == {
        "user": {"id": ANY, "name": "John"},
        "token": ANY,
        "errors": None,
    }

    # Mutation creates user account
    user_from_db = await User.query.one(id=int(data["user"]["id"]))
    assert user_from_db.is_active
    assert not user_from_db.is_moderator
    assert not user_from_db.is_admin
    assert await check_password(" password123 ", user_from_db.password)

    # Mutation creates user token
    user_from_token = await get_user_from_token(graphql_info.context, data["token"])
    assert user_from_token.id == int(data["user"]["id"])


@pytest.mark.asyncio
@override_dynamic_settings(password_min_length=10)
async def test_user_create_mutation_validates_min_password_length(query_public_api, db):
    result = await query_public_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "abcd",
                "email": "john@example.com",
                "password": "pass",
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": "password",
                "type": "value_error.any_str.min_length",
            }
        ],
    }


@pytest.mark.asyncio
async def test_user_create_mutation_validates_max_password_length(query_public_api, db):
    result = await query_public_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "abcd",
                "email": "john@example.com",
                "password": "p" * 60,
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": "password",
                "type": "value_error.any_str.max_length",
            }
        ],
    }


@pytest.mark.asyncio
@override_dynamic_settings(username_min_length=10)
async def test_user_create_mutation_validates_min_user_name_length(
    query_public_api, db
):
    result = await query_public_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "abcd",
                "email": "john@example.com",
                "password": " password123 ",
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": "name",
                "type": "value_error.any_str.min_length",
            }
        ],
    }


@pytest.mark.asyncio
@override_dynamic_settings(username_min_length=1, username_max_length=3)
async def test_user_create_mutation_validates_max_user_name_length(
    query_public_api, db
):
    result = await query_public_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "abcd",
                "email": "john@example.com",
                "password": " password123 ",
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": "name",
                "type": "value_error.any_str.max_length",
            }
        ],
    }


@pytest.mark.asyncio
async def test_user_create_mutation_validates_user_name_content(query_public_api, db):
    result = await query_public_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "invalid!",
                "email": "john@example.com",
                "password": " password123 ",
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": "name",
                "type": "value_error.username",
            }
        ],
    }


@pytest.mark.asyncio
async def test_user_create_mutation_validates_if_username_is_available(
    query_public_api, user
):
    result = await query_public_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": user.name,
                "email": "john@example.com",
                "password": " password123 ",
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": "name",
                "type": "value_error.username.not_available",
            }
        ],
    }


@pytest.mark.asyncio
async def test_user_create_mutation_validates_user_email(query_public_api, db):
    result = await query_public_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "John",
                "email": "invalidemail",
                "password": " password123 ",
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": "email",
                "type": "value_error.email",
            }
        ],
    }


@pytest.mark.asyncio
async def test_user_create_mutation_validates_if_user_email_is_available(
    query_public_api, user
):
    result = await query_public_api(
        USER_CREATE_MUTATION,
        {
            "input": {
                "name": "John",
                "email": user.email,
                "password": " password123 ",
            },
        },
    )

    assert result["data"]["userCreate"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": "email",
                "type": "value_error.email.not_available",
            }
        ],
    }
