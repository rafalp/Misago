from typing import Any, Awaitable, Callable, Dict, Optional

from ...context import Context
from ...hooks import FilterHook
from ...users.models import User

GetUserFromTokenAction = Callable[[Context, str, bool], Awaitable[Optional[User]]]
GetUserFromTokenFilter = Callable[
    [GetUserFromTokenAction, Context, str, bool],
    Awaitable[Optional[User]],
]


class GetUserFromTokenHook(FilterHook[GetUserFromTokenAction, GetUserFromTokenFilter]):
    def call_action(
        self,
        action: GetUserFromTokenAction,
        context: Context,
        token: str,
        in_admin: bool,
    ) -> Awaitable[Optional[User]]:
        return self.filter(action, context, token, in_admin)


GetUserFromTokenPayloadAction = Callable[
    [Context, Dict[str, Any], bool], Awaitable[Optional[User]]
]
GetUserFromTokenPayloadFilter = Callable[
    [GetUserFromTokenPayloadAction, Context, Dict[str, Any], bool],
    Awaitable[Optional[User]],
]


class GetUserFromTokenPayloadHook(
    FilterHook[GetUserFromTokenPayloadAction, GetUserFromTokenPayloadFilter]
):
    def call_action(
        self,
        action: GetUserFromTokenPayloadAction,
        context: Context,
        token_payload: Dict[str, Any],
        in_admin: bool,
    ) -> Awaitable[Optional[User]]:
        return self.filter(action, context, token_payload, in_admin)


get_user_from_token_hook = GetUserFromTokenHook()
get_user_from_token_payload_hook = GetUserFromTokenPayloadHook()
