from unittest.mock import Mock

import pytest

from ..auth import (
    AUTHORIZATION_HEADER,
    AUTHORIZATION_TYPE,
    get_authenticated_admin,
    get_authenticated_user,
    get_user_from_context,
)
from ..token import create_user_token


@pytest.mark.asyncio
async def test_user_is_retrieved_from_context_with_valid_auth_token(
    dynamic_settings, user
):
    token = await create_user_token({"settings": dynamic_settings}, user)
    request = Mock(headers={AUTHORIZATION_HEADER: f"{AUTHORIZATION_TYPE} {token}"})
    context_user = await get_user_from_context(
        {"settings": dynamic_settings, "request": request}
    )
    assert context_user == user


@pytest.mark.asyncio
async def test_no_user_is_retrieved_from_context_without_auth_header(
    dynamic_settings, user
):
    request = Mock(headers={})
    context_user = await get_user_from_context(
        {"settings": dynamic_settings, "request": request}
    )
    assert context_user is None


@pytest.mark.asyncio
async def test_no_user_is_retrieved_from_context_with_invalid_auth_header(
    dynamic_settings, user
):
    request = Mock(headers={AUTHORIZATION_HEADER: "invalid"})
    context_user = await get_user_from_context(
        {"settings": dynamic_settings, "request": request}
    )
    assert context_user is None


@pytest.mark.asyncio
async def test_no_user_is_retrieved_from_context_with_invalid_auth_token_type(
    dynamic_settings, user
):
    token = await create_user_token({"settings": dynamic_settings}, user)
    request = Mock(headers={AUTHORIZATION_HEADER: f"JWT {token}"})
    context_user = await get_user_from_context(
        {"settings": dynamic_settings, "request": request}
    )
    assert context_user is None


@pytest.mark.asyncio
async def test_no_user_is_retrieved_from_context_with_invalid_auth_token(
    dynamic_settings, user
):
    request = Mock(headers={AUTHORIZATION_HEADER: f"{AUTHORIZATION_TYPE} invalid"})
    context_user = await get_user_from_context(
        {"settings": dynamic_settings, "request": request}
    )
    assert context_user is None


@pytest.mark.asyncio
async def test_admin_is_retrieved_from_context_with_valid_auth_token(
    dynamic_settings, admin
):
    token = await create_user_token({"settings": dynamic_settings}, admin)
    request = Mock(headers={AUTHORIZATION_HEADER: f"{AUTHORIZATION_TYPE} {token}"})
    context_user = await get_authenticated_admin(
        {"settings": dynamic_settings, "request": request}
    )
    assert context_user == admin


@pytest.mark.asyncio
async def test_admin_is_not_retrieved_from_context_with_valid_non_admin_auth_token(
    dynamic_settings, user
):
    token = await create_user_token({"settings": dynamic_settings}, user)
    request = Mock(headers={AUTHORIZATION_HEADER: f"{AUTHORIZATION_TYPE} {token}"})
    context_user = await get_authenticated_admin(
        {"settings": dynamic_settings, "request": request}
    )
    assert context_user is None


@pytest.mark.asyncio
async def test_context_user_is_rechecked_when_authenticated_admin_is_retrieved(
    dynamic_settings, user
):
    token = await create_user_token({"settings": dynamic_settings}, user)
    request = Mock(headers={AUTHORIZATION_HEADER: f"{AUTHORIZATION_TYPE} {token}"})
    context = {"settings": dynamic_settings, "request": request}
    context_user = await get_authenticated_user(context)
    assert context_user == user
    context_admin = await get_authenticated_admin(context)
    assert context_admin is None
