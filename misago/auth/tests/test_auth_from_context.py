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
async def test_user_is_retrieved_from_context_with_valid_auth_token(context, user):
    token = await create_user_token(context, user)
    request = Mock(headers={AUTHORIZATION_HEADER: f"{AUTHORIZATION_TYPE} {token}"})
    context["request"] = request

    context_user = await get_user_from_context(context)
    assert context_user == user


@pytest.mark.asyncio
async def test_no_user_is_retrieved_from_context_without_auth_header(context, user):
    request = Mock(headers={})
    context["request"] = request

    context_user = await get_user_from_context(context)
    assert context_user is None


@pytest.mark.asyncio
async def test_no_user_is_retrieved_from_context_with_invalid_auth_header(
    context, user
):
    request = Mock(headers={AUTHORIZATION_HEADER: "invalid"})
    context["request"] = request

    context_user = await get_user_from_context(context)
    assert context_user is None


@pytest.mark.asyncio
async def test_no_user_is_retrieved_from_context_with_invalid_auth_token_type(
    context, user
):
    token = await create_user_token(context, user)
    request = Mock(headers={AUTHORIZATION_HEADER: f"JWT {token}"})
    context["request"] = request

    context_user = await get_user_from_context(context)
    assert context_user is None


@pytest.mark.asyncio
async def test_no_user_is_retrieved_from_context_with_invalid_auth_token(context, user):
    request = Mock(headers={AUTHORIZATION_HEADER: f"{AUTHORIZATION_TYPE} invalid"})
    context["request"] = request

    context_user = await get_user_from_context(context)
    assert context_user is None


@pytest.mark.asyncio
async def test_admin_is_retrieved_from_context_with_valid_auth_token(context, admin):
    token = await create_user_token(context, admin)
    request = Mock(headers={AUTHORIZATION_HEADER: f"{AUTHORIZATION_TYPE} {token}"})
    context["request"] = request

    context_user = await get_authenticated_admin(context)
    assert context_user == admin


@pytest.mark.asyncio
async def test_admin_is_not_retrieved_from_context_with_valid_non_admin_auth_token(
    context, user
):
    token = await create_user_token(context, user)
    request = Mock(headers={AUTHORIZATION_HEADER: f"{AUTHORIZATION_TYPE} {token}"})
    context["request"] = request

    context_user = await get_authenticated_admin(context)
    assert context_user is None


@pytest.mark.asyncio
async def test_context_user_is_rechecked_when_authenticated_admin_is_retrieved(
    context, user
):
    token = await create_user_token(context, user)
    request = Mock(headers={AUTHORIZATION_HEADER: f"{AUTHORIZATION_TYPE} {token}"})
    context["request"] = request

    context_user = await get_authenticated_user(context)
    assert context_user == user

    context_admin = await get_authenticated_admin(context)
    assert context_admin is None
