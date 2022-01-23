from typing import Any, Awaitable, Callable, Dict, Optional

from ...graphql import GraphQLContext
from ...hooks import FilterHook
from ...users.models import User

GetUserFromTokenAction = Callable[
    [GraphQLContext, str, bool], Awaitable[Optional[User]]
]
GetUserFromTokenFilter = Callable[
    [GetUserFromTokenAction, GraphQLContext, str, bool],
    Awaitable[Optional[User]],
]


class GetUserFromTokenHook(FilterHook[GetUserFromTokenAction, GetUserFromTokenFilter]):
    def call_action(
        self,
        action: GetUserFromTokenAction,
        context: GraphQLContext,
        token: str,
        in_admin: bool,
    ) -> Awaitable[Optional[User]]:
        return self.filter(action, context, token, in_admin)


GetUserFromTokenPayloadAction = Callable[
    [GraphQLContext, Dict[str, Any], bool], Awaitable[Optional[User]]
]
GetUserFromTokenPayloadFilter = Callable[
    [GetUserFromTokenPayloadAction, GraphQLContext, Dict[str, Any], bool],
    Awaitable[Optional[User]],
]


class GetUserFromTokenPayloadHook(
    FilterHook[GetUserFromTokenPayloadAction, GetUserFromTokenPayloadFilter]
):
    def call_action(
        self,
        action: GetUserFromTokenPayloadAction,
        context: GraphQLContext,
        token_payload: Dict[str, Any],
        in_admin: bool,
    ) -> Awaitable[Optional[User]]:
        return self.filter(action, context, token_payload, in_admin)


get_user_from_token_hook = GetUserFromTokenHook()
get_user_from_token_payload_hook = GetUserFromTokenPayloadHook()
