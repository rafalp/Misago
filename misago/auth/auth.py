from typing import Optional

from ..hooks import get_user_from_context_hook, get_user_from_token_hook
from ..types import GraphQLContext, User
from .token import get_user_from_token


AUTHORIZATION_HEADER = "authorization"
AUTHORIZATION_TYPE = "bearer"
TOKEN_ENCODING = "latin-1"


async def authenticate(
    context: GraphQLContext, username: str, password: str
) -> Optional[User]:
    return None  # TODO


async def get_authenticated_user(context: GraphQLContext) -> Optional[User]:
    if "user" not in context:
        context["user"] = await get_user_from_context_hook.call_action(
            get_user_from_context, context
        )

    return context["user"]


async def get_user_from_context(context: GraphQLContext) -> Optional[User]:
    headers = context["request"].headers
    authorization = headers.get(AUTHORIZATION_HEADER)
    if not authorization:
        return None

    token = get_auth_token(authorization)
    if not token:
        return None

    return await get_user_from_token_hook.call_action(
        get_user_from_token, context, token
    )


def get_auth_token(header: str) -> Optional[bytes]:
    token_parts = header.split(" ")
    if len(token_parts) != 2:
        return None

    if token_parts[0].lower() != AUTHORIZATION_TYPE:
        return None

    return token_parts[1].encode(TOKEN_ENCODING) or None
