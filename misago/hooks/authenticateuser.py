from typing import Optional

from ..types import AuthenticateUserAction, AuthenticateUserFilter, GraphQLContext, User
from .filter import FilterHook


class AuthenticateUserHook(FilterHook[AuthenticateUserAction, AuthenticateUserFilter]):
    async def call_action(
        self,
        action: AuthenticateUserAction,
        context: GraphQLContext,
        username: str,
        password: str,
        in_admin: bool,
    ) -> Optional[User]:
        return await self.filter(action, context, username, password, in_admin)
