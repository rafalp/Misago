from typing import Awaitable, Optional

from ..graphql import GraphQLContext
from ..passwords import check_password
from ..users.get import get_user_by_name_or_email
from ..users.models import User
from .hooks import (
    authenticate_user_hook,
    get_user_from_context_hook,
    get_user_from_token_hook,
)
from .token import get_user_from_token

__all__ = [
    "AUTHORIZATION_HEADER",
    "AUTHORIZATION_TYPE",
    "authenticate_user",
    "get_authenticated_user",
    "get_authenticated_admin",
]

AUTHORIZATION_HEADER = "authorization"
AUTHORIZATION_TYPE = "bearer"


def authenticate_user(
    context: GraphQLContext, username: str, password: str, in_admin: bool = False
) -> Awaitable[Optional[User]]:
    return authenticate_user_hook.call_action(
        authenticate_user_action, context, username, password, in_admin
    )


async def authenticate_user_action(
    context: GraphQLContext, username: str, password: str, in_admin: bool = False
) -> Optional[User]:
    user = await get_user_by_name_or_email(username)

    if not user or not user.is_active:
        return None
    if user.password is None or not await check_password(password, user.password):
        return None

    return user


def get_authenticated_user(context: GraphQLContext) -> Awaitable[Optional[User]]:
    return get_user_from_context_hook.call_action(
        get_user_from_context, context, in_admin=False
    )


def get_authenticated_admin(context: GraphQLContext) -> Awaitable[Optional[User]]:
    return get_user_from_context_hook.call_action(
        get_user_from_context, context, in_admin=True
    )


async def get_user_from_context(
    context: GraphQLContext, in_admin: bool = False
) -> Optional[User]:
    headers = context["request"].headers
    authorization = headers.get(AUTHORIZATION_HEADER)
    if not authorization:
        return None

    token = get_auth_token(authorization)
    if not token:
        return None

    user = await get_user_from_token_hook.call_action(
        get_user_from_token, context, token, in_admin
    )

    if in_admin and user and not user.is_admin:
        return None

    return user


def get_auth_token(header: str) -> Optional[str]:
    token_parts = header.split(" ")
    if len(token_parts) != 2:
        return None

    if token_parts[0].lower() != AUTHORIZATION_TYPE:
        return None

    return token_parts[1] or None
