from typing import Optional

from ..graphql import GraphQLContext
from ..loaders import load_user
from ..users.models import User


async def get_user(
    context: GraphQLContext, user_id: int, in_admin: bool = False
) -> Optional[User]:
    user = await load_user(context, user_id)
    if not user or not user.is_active:
        return None
    return user
