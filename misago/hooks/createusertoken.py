from typing import Any, Dict

from ..types import (
    CreateUserTokenAction,
    CreateUserTokenFilter,
    CreateUserTokenPayloadAction,
    CreateUserTokenPayloadFilter,
    GraphQLContext,
    User,
)
from .filter import FilterHook


class CreateUserTokenHook(FilterHook[CreateUserTokenAction, CreateUserTokenFilter]):
    async def call_action(
        self,
        action: CreateUserTokenAction,
        context: GraphQLContext,
        user: User,
        in_admin: bool,
    ) -> str:
        return await self.filter(action, context, user, in_admin)


class CreateUserTokenPayloadHook(
    FilterHook[CreateUserTokenPayloadAction, CreateUserTokenPayloadFilter]
):
    async def call_action(
        self,
        action: CreateUserTokenPayloadAction,
        context: GraphQLContext,
        user: User,
        in_admin: bool,
    ) -> Dict[str, Any]:
        return await self.filter(action, context, user, in_admin)
