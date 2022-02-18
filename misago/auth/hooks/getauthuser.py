from typing import Awaitable, Callable, Optional

from ...context import Context
from ...hooks import FilterHook
from ...users.models import User

GetAuthUserAction = Callable[[Context, int], Awaitable[Optional[User]]]
GetAuthUserFilter = Callable[
    [GetAuthUserAction, Context, int], Awaitable[Optional[User]]
]


class GetAuthUserHook(FilterHook[GetAuthUserAction, GetAuthUserFilter]):
    def call_action(
        self,
        action: GetAuthUserAction,
        context: Context,
        user_id: int,
        in_admin: bool = False,
    ) -> Awaitable[Optional[User]]:
        return self.filter(action, context, user_id, in_admin)


get_auth_user_hook = GetAuthUserHook()
