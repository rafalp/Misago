from typing import Awaitable, Callable, Optional

from ...context import Context
from ...hooks import FilterHook

GetAnonymousPermissionsAction = Callable[[Context], Awaitable[dict]]
GetAnonymousPermissionsFilter = Callable[
    [GetAnonymousPermissionsAction, Context], Awaitable[dict]
]


class GetAnonymousPermissionsHook(
    FilterHook[GetAnonymousPermissionsAction, GetAnonymousPermissionsFilter]
):
    def call_action(
        self,
        action: GetAnonymousPermissionsAction,
        context: Context,
    ) -> Awaitable[dict]:
        return self.filter(action, context)


get_anonymous_permissions_hook = GetAnonymousPermissionsHook()
