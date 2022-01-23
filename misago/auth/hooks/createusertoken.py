from typing import Any, Awaitable, Callable, Dict

from ...graphql import GraphQLContext
from ...hooks import FilterHook
from ...users.models import User

CreateUserTokenAction = Callable[[GraphQLContext, User, bool], Awaitable[str]]
CreateUserTokenFilter = Callable[
    [CreateUserTokenAction, GraphQLContext, User, bool], Awaitable[str]
]


class CreateUserTokenHook(FilterHook[CreateUserTokenAction, CreateUserTokenFilter]):
    def call_action(
        self,
        action: CreateUserTokenAction,
        context: GraphQLContext,
        user: User,
        in_admin: bool,
    ) -> Awaitable[str]:
        return self.filter(action, context, user, in_admin)


CreateUserTokenPayloadAction = Callable[
    [GraphQLContext, User, bool], Awaitable[Dict[str, Any]]
]
CreateUserTokenPayloadFilter = Callable[
    [CreateUserTokenPayloadAction, GraphQLContext, User, bool],
    Awaitable[Dict[str, Any]],
]


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


create_user_token_hook = CreateUserTokenHook()
create_user_token_payload_hook = CreateUserTokenPayloadHook()
