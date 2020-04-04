from typing import Optional

from ..types import AuthenticateUserAction, AuthenticateUserFilter, GraphQLContext, User
from .filter import FilterHook


class AuthenticateAdminHook(FilterHook[AuthenticateUserAction, AuthenticateUserFilter]):
    async def call_action(
        self,
        action: AuthenticateUserAction,
        context: GraphQLContext,
        username: str,
        password: str,
    ) -> Optional[User]:
        return await self.filter(action, context, username, password)
