from typing import Any, Dict, Optional

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
    async def call_action(
        self, action: GetAuthUserAction, context: GraphQLContext, user_id: int
    ) -> Optional[User]:
        return await self.filter(action, context, user_id)


class GetUserFromContextHook(
    FilterHook[GetUserFromContextAction, GetUserFromContextFilter]
):
    async def call_action(
        self, action: GetUserFromContextAction, context: GraphQLContext
    ) -> Optional[User]:
        return await self.filter(action, context)


class GetUserFromTokenHook(FilterHook[GetUserFromTokenAction, GetUserFromTokenFilter]):
    async def call_action(
        self, action: GetUserFromTokenAction, context: GraphQLContext, token: str
    ) -> Optional[User]:
        return await self.filter(action, context, token)


class GetUserFromTokenPayloadHook(
    FilterHook[GetUserFromTokenPayloadAction, GetUserFromTokenPayloadFilter]
):
    async def call_action(
        self,
        action: GetUserFromTokenPayloadAction,
        context: GraphQLContext,
        token_payload: Dict[str, Any],
    ) -> Optional[User]:
        return await self.filter(action, context, token_payload)
