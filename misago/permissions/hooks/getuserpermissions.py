from typing import Awaitable, Callable

from ...context import Context
from ...hooks import FilterHook
from ...users.models import User

GetUserPermissionsAction = Callable[[Context, User], Awaitable[dict]]
GetUserPermissionsFilter = Callable[
    [GetUserPermissionsAction, Context, User], Awaitable[dict]
]


class GetUserPermissionsHook(
    FilterHook[GetUserPermissionsAction, GetUserPermissionsFilter]
):
    def call_action(
        self,
        action: GetUserPermissionsAction,
        context: Context,
        user: User,
    ) -> Awaitable[dict]:
        return self.filter(action, context, user)


get_user_permissions_hook = GetUserPermissionsHook()
