from unittest.mock import ANY

import pytest

from .....auth import get_user_from_token
from .....conf.dynamicsettings import get_settings_from_db
from .....passwords import check_password
from .....testing import override_dynamic_settings
from .....users.get import get_user_by_email
from .....users.models import User
from ..setupsite import resolve_setup_site


@pytest.mark.asyncio
async def test_setup_site_mutation_disables_site_wizard(db, graphql_info):
    data = await resolve_setup_site(
        None,
        graphql_info,
        input={
            "forumName": "Hello world!",
            "forumIndexThreads": False,
            "name": "John",
            "email": "john@example.com",
            "password": " password123 ",
        },
    )

    assert not "errors" in data

    settings = await get_settings_from_db()
    assert not settings["enable_site_wizard"]


@pytest.mark.asyncio
async def test_setup_site_mutation_updates_initial_settings(db, graphql_info):
    data = await resolve_setup_site(
        None,
        graphql_info,
        input={
            "forumName": "Hello world!",
            "forumIndexThreads": False,
            "name": "John",
            "email": "john@example.com",
            "password": " password123 ",
        },
    )

    assert not "errors" in data

    settings = await get_settings_from_db()
    assert settings["forum_name"] == "Hello world!"
    assert settings["forum_index_threads"] is False


@pytest.mark.asyncio
async def test_setup_site_mutation_creates_admin_account(db, graphql_info):
    data = await resolve_setup_site(
        None,
        graphql_info,
        input={
            "forumName": "Hello world!",
            "forumIndexThreads": False,
            "name": "John",
            "email": "john@example.com",
            "password": " password123 ",
        },
    )

    assert not "errors" in data

    assert data["user"] == await User.query.one(id=data["user"].id)
    assert await check_password(" password123 ", data["user"].password)


@pytest.mark.asyncio
async def test_setup_site_mutation_returns_admin_token(db, graphql_info):
    data = await resolve_setup_site(
        None,
        graphql_info,
        input={
            "forumName": "Hello world!",
            "forumIndexThreads": False,
            "name": "John",
            "email": "john@example.com",
            "password": " password123 ",
        },
    )

    assert not "errors" in data
    assert "token" in data

    user_from_token = await get_user_from_token(graphql_info.context, data["token"])
    assert user_from_token.id == data["user"].id


@pytest.mark.asyncio
@override_dynamic_settings(enable_site_wizard=False)
async def test_setup_site_mutation_returns_error_if_site_wizard_is_disabled(
    db, graphql_info
):
    data = await resolve_setup_site(
        None,
        graphql_info,
        input={
            "forumName": "Hello world!",
            "forumIndexThreads": False,
            "name": "John",
            "email": "john@example.com",
            "password": " password123 ",
        },
    )

    assert data == {
        "errors": [
            {
                "loc": ("__root__",),
                "type": "value_error.site_wizard.disabled",
                "msg": "site wizard is disabled",
            }
        ]
    }

    user = await get_user_by_email("john@example.com")
    assert user is None


@pytest.mark.asyncio
async def test_setup_site_mutation_validates_user_name(db, graphql_info):
    data = await resolve_setup_site(
        None,
        graphql_info,
        input={
            "forumName": "Hello world!",
            "forumIndexThreads": False,
            "name": "!!!",
            "email": "john@example.com",
            "password": " password123 ",
        },
    )

    assert data == {
        "errors": [
            {
                "loc": ("name",),
                "type": "value_error.username",
                "msg": ANY,
                "ctx": ANY,
            }
        ]
    }


@pytest.mark.asyncio
async def test_setup_site_mutation_validates_user_namel_is_available(
    db, graphql_info, user
):
    data = await resolve_setup_site(
        None,
        graphql_info,
        input={
            "forumName": "Hello world!",
            "forumIndexThreads": False,
            "name": user.name,
            "email": "john@example.com",
            "password": " password123 ",
        },
    )

    assert data == {
        "errors": [
            {
                "loc": ("name",),
                "type": "value_error.username.not_available",
                "msg": "username is not available",
            }
        ]
    }


@pytest.mark.asyncio
async def test_setup_site_mutation_validates_user_email(db, graphql_info):
    data = await resolve_setup_site(
        None,
        graphql_info,
        input={
            "forumName": "Hello world!",
            "forumIndexThreads": False,
            "name": "John",
            "email": "invalidemail",
            "password": " password123 ",
        },
    )

    assert data == {
        "errors": [
            {
                "loc": ("email",),
                "type": "value_error.email",
                "msg": "value is not a valid email address",
            }
        ]
    }


@pytest.mark.asyncio
async def test_setup_site_mutation_validates_user_email_is_available(
    db, graphql_info, user
):
    data = await resolve_setup_site(
        None,
        graphql_info,
        input={
            "forumName": "Hello world!",
            "forumIndexThreads": False,
            "name": "John",
            "email": user.email,
            "password": " password123 ",
        },
    )

    assert data == {
        "errors": [
            {
                "loc": ("email",),
                "type": "value_error.email.not_available",
                "msg": "e-mail is not available",
            }
        ]
    }
