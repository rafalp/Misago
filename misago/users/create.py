from typing import Optional

from ..graphql import GraphQLContext
from .hooks import create_user_hook
from .models import User


async def create_user(
    name: str,
    email: str,
    *,
    password: Optional[str] = None,
    is_active: bool = True,
    is_moderator: bool = False,
    is_admin: bool = False,
    context: Optional[GraphQLContext] = None,
) -> User:
    return await create_user_hook.call_action(
        User.create,
        name,
        email,
        password=password,
        is_active=is_active,
        is_moderator=is_moderator,
        is_admin=is_admin,
        extra={},
        context=context,
    )
