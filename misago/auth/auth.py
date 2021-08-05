from typing import Optional

from ..graphql import GraphQLContext
from ..passwords import check_password
from ..users.get import get_user_by_name_or_email
from ..users.models import User
from .hooks import get_user_from_context_hook, get_user_from_token_hook
from .token import get_user_from_token

AUTHORIZATION_HEADER = "authorization"
AUTHORIZATION_TYPE = "bearer"


async def authenticate_user(
    context: GraphQLContext, username: str, password: str, in_admin: bool = False
) -> Optional[User]:
    user = await get_user_by_name_or_email(username)

    if not user or not user.is_active:
        return None
    if user.password is None or not await check_password(password, user.password):
        return None

    return user


async def get_authenticated_user(context: GraphQLContext) -> Optional[User]:
    if "user" not in context:
        context["user"] = await get_user_from_context_hook.call_action(
            get_user_from_context, context, in_admin=False
        )

    return context["user"]


async def get_authenticated_admin(context: GraphQLContext) -> Optional[User]:
    if "checked_admin_auth" not in context:
        context["checked_admin_auth"] = True
        context["user"] = await get_user_from_context_hook.call_action(
            get_user_from_context, context, in_admin=True
        )
    if context["user"] and context["user"].is_admin:
        return context["user"]
    return None


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

    return await get_user_from_token_hook.call_action(
        get_user_from_token, context, token, in_admin
    )


def get_auth_token(header: str) -> Optional[str]:
    token_parts = header.split(" ")
    if len(token_parts) != 2:
        return None

    if token_parts[0].lower() != AUTHORIZATION_TYPE:
        return None

    return token_parts[1] or None
