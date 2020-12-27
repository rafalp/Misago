from typing import Any, Awaitable, Dict, Optional

from ..types import (
    GetAuthUserAction,
    GetAuthUserFilter,
    GetUserFromContextAction,
    GetUserFromContextFilter,
    GetUserFromTokenAction,
    GetUserFromTokenFilter,
    GetUserFromTokenPayloadAction,
    GetUserFromTokenPayloadFilter,
    GraphQLContext,
    User,
)
from .filter import FilterHook


class GetAuthUserHook(FilterHook[GetAuthUserAction, GetAuthUserFilter]):
    def call_action(
        self,
        action: GetAuthUserAction,
        context: GraphQLContext,
        user_id: int,
        in_admin: bool = False,
    ) -> Awaitable[Optional[User]]:
        return self.filter(action, context, user_id, in_admin)


class GetUserFromContextHook(
    FilterHook[GetUserFromContextAction, GetUserFromContextFilter]
):
    def call_action(
        self, action: GetUserFromContextAction, context: GraphQLContext, in_admin: bool
    ) -> Awaitable[Optional[User]]:
        return self.filter(action, context, in_admin)


class GetUserFromTokenHook(FilterHook[GetUserFromTokenAction, GetUserFromTokenFilter]):
    def call_action(
        self,
        action: GetUserFromTokenAction,
        context: GraphQLContext,
        token: str,
        in_admin: bool,
    ) -> Awaitable[Optional[User]]:
        return self.filter(action, context, token, in_admin)


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
