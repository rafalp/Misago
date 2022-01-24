from typing import Optional, cast

from ..graphql import GraphQLContext
from .hooks.createuser import CreateUserAction, create_user_hook
from .models import User


async def create_user(
    context: GraphQLContext,
    name: str,
    email: str,
    *,
    password: Optional[str] = None,
    is_active: bool = True,
    is_moderator: bool = False,
    is_admin: bool = False,
) -> User:
    return await create_user_hook.call_action(
        cast(CreateUserAction, User.create),
        name,
        email,
        password=password,
        is_active=is_active,
        is_moderator=is_moderator,
        is_admin=is_admin,
        extra={},
        context=context,
    )
