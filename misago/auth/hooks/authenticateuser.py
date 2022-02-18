from typing import Awaitable, Callable, Optional

from ...context import Context
from ...hooks import FilterHook
from ...users.models import User

AuthenticateUserAction = Callable[[Context, str, str, bool], Awaitable[Optional[User]]]
AuthenticateUserFilter = Callable[
    [AuthenticateUserAction, Context, str, str, bool], Awaitable[Optional[User]]
]


class AuthenticateUserHook(FilterHook[AuthenticateUserAction, AuthenticateUserFilter]):
    def call_action(
        self,
        action: AuthenticateUserAction,
        context: Context,
        username: str,
        password: str,
        in_admin: bool,
    ) -> Awaitable[Optional[User]]:
        return self.filter(action, context, username, password, in_admin)


authenticate_user_hook = AuthenticateUserHook()
