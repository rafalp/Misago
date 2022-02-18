from typing import Awaitable, Callable, Optional

from ...context import Context
from ...hooks import FilterHook
from ...users.models import User

GetUserFromContextAction = Callable[[Context, bool], Awaitable[Optional[User]]]
GetUserFromContextFilter = Callable[
    [GetUserFromContextAction, Context, bool],
    Awaitable[Optional[User]],
]


class GetUserFromContextHook(
    FilterHook[GetUserFromContextAction, GetUserFromContextFilter]
):
    def call_action(
        self, action: GetUserFromContextAction, context: Context, in_admin: bool
    ) -> Awaitable[Optional[User]]:
        return self.filter(action, context, in_admin)


get_user_from_context_hook = GetUserFromContextHook()
