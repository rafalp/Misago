from unittest.mock import ANY

import pytest

from .....auth import get_user_from_token
from .....conf.dynamicsettings import get_settings_from_db
from .....errors import ErrorsList
from .....passwords import check_password
from .....testing import override_dynamic_settings
from .....users.get import get_user_by_email
from .....users.models import User

SITE_SETUP_MUTATION = """
    mutation SiteSetup($input: SiteSetupInput!) {
        siteSetup(input: $input) {
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
async def test_setup_site_mutation_setups_site(query_public_api, graphql_info, db):
    result = await query_public_api(
        SITE_SETUP_MUTATION,
        {
            "input": {
                "forumName": "Hello world!",
                "forumIndexThreads": False,
                "name": "John",
                "email": "john@example.com",
                "password": " password123 ",
            },
        },
    )

    data = result["data"]["siteSetup"]

    assert data == {
        "user": {"id": ANY, "name": "John"},
        "token": ANY,
        "errors": None,
    }

    settings = await get_settings_from_db()
    assert not settings["enable_site_wizard"], "Site wizard should disable after use"
    assert settings["forum_name"] == "Hello world!"
    assert settings["forum_index_threads"] is False

    # Wizard creates admin account
    user_from_db = await User.query.one(id=int(data["user"]["id"]))
    assert user_from_db.is_active
    assert user_from_db.is_moderator
    assert user_from_db.is_admin
    assert await check_password(" password123 ", user_from_db.password)

    # Wizard creates admin token
    user_from_token = await get_user_from_token(graphql_info.context, data["token"])
    assert user_from_token.id == int(data["user"]["id"])


@pytest.mark.asyncio
@override_dynamic_settings(enable_site_wizard=False)
async def test_setup_site_mutation_returns_error_if_site_wizard_is_disabled(
    query_public_api, db
):
    result = await query_public_api(
        SITE_SETUP_MUTATION,
        {
            "input": {
                "forumName": "Hello world!",
                "forumIndexThreads": False,
                "name": "John",
                "email": "john@example.com",
                "password": " password123 ",
            },
        },
    )

    assert result["data"]["siteSetup"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": ErrorsList.ROOT_LOCATION,
                "type": "value_error.site_wizard.disabled",
            },
        ],
    }

    user = await get_user_by_email("john@example.com")
    assert user is None


@pytest.mark.asyncio
async def test_setup_site_mutation_validates_user_name(query_public_api, db):
    result = await query_public_api(
        SITE_SETUP_MUTATION,
        {
            "input": {
                "forumName": "Hello world!",
                "forumIndexThreads": False,
                "name": "!!!",
                "email": "john@example.com",
                "password": " password123 ",
            },
        },
    )

    assert result["data"]["siteSetup"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": "name",
                "type": "value_error.username",
            },
        ],
    }


@pytest.mark.asyncio
async def test_setup_site_mutation_validates_user_name_is_available(
    query_public_api, user
):
    result = await query_public_api(
        SITE_SETUP_MUTATION,
        {
            "input": {
                "forumName": "Hello world!",
                "forumIndexThreads": False,
                "name": user.name,
                "email": "john@example.com",
                "password": " password123 ",
            },
        },
    )

    assert result["data"]["siteSetup"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": "name",
                "type": "value_error.username.not_available",
            },
        ],
    }


@pytest.mark.asyncio
async def test_setup_site_mutation_validates_user_email(query_public_api, db):
    result = await query_public_api(
        SITE_SETUP_MUTATION,
        {
            "input": {
                "forumName": "Hello world!",
                "forumIndexThreads": False,
                "name": "John",
                "email": "invalidemail",
                "password": " password123 ",
            },
        },
    )

    assert result["data"]["siteSetup"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": "email",
                "type": "value_error.email",
            },
        ],
    }


@pytest.mark.asyncio
async def test_setup_site_mutation_validates_user_email_is_available(
    query_public_api, user
):
    result = await query_public_api(
        SITE_SETUP_MUTATION,
        {
            "input": {
                "forumName": "Hello world!",
                "forumIndexThreads": False,
                "name": "John",
                "email": user.email,
                "password": " password123 ",
            },
        },
    )

    assert result["data"]["siteSetup"] == {
        "user": None,
        "token": None,
        "errors": [
            {
                "location": "email",
                "type": "value_error.email.not_available",
            },
        ],
    }
