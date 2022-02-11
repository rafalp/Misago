from typing import Optional

from ..graphql import GraphQLContext
from ..users.loaders import users_loader
from ..users.models import User


async def get_user(
    context: GraphQLContext, user_id: int, in_admin: bool = False
) -> Optional[User]:
    user = await users_loader.load(context, user_id)
    if not user or not user.is_active:
        return None
    return user
