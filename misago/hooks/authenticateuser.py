from typing import Awaitable, Optional

from ..types import AuthenticateUserAction, AuthenticateUserFilter, GraphQLContext, User
from .filter import FilterHook


class AuthenticateUserHook(FilterHook[AuthenticateUserAction, AuthenticateUserFilter]):
    def call_action(
        self,
        action: AuthenticateUserAction,
        context: GraphQLContext,
        username: str,
        password: str,
        in_admin: bool,
    ) -> Awaitable[Optional[User]]:
        return self.filter(action, context, username, password, in_admin)
