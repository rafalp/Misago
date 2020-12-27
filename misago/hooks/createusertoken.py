from typing import Any, Awaitable, Dict

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
    def call_action(
        self,
        action: CreateUserTokenAction,
        context: GraphQLContext,
        user: User,
        in_admin: bool,
    ) -> Awaitable[str]:
        return self.filter(action, context, user, in_admin)


class CreateUserTokenPayloadHook(
    FilterHook[CreateUserTokenPayloadAction, CreateUserTokenPayloadFilter]
):
    def call_action(
        self,
        action: CreateUserTokenPayloadAction,
        context: GraphQLContext,
        user: User,
        in_admin: bool,
    ) -> Awaitable[Dict[str, Any]]:
        return self.filter(action, context, user, in_admin)
