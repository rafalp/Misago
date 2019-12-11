from typing import Optional

from ..loaders import load_user
from ..types import GraphQLContext, User


AUTHORIZATION_HEADER = "authorization"


async def authenticate(
    context: GraphQLContext, username: str, password: str
) -> Optional[User]:
    return None  # TODO


async def get_context_user(context: GraphQLContext) -> Optional[User]:
    headers = context["request"].headers
    authorization = headers.get(AUTHORIZATION_HEADER)
    if not authorization:
        return None

    return None  # TODO


async def get_user(context: GraphQLContext, user_id: int) -> Optional[User]:
    user = await load_user(context, user_id)
    if user and user.is_deactivated:
        return None
    return user
