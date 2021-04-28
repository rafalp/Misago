from typing import Any, Awaitable, Callable, Dict, Optional

from ..graphql import GraphQLContext
from ..hooks import FilterHook
from ..users.models import User


AuthenticateUserAction = Callable[
    [GraphQLContext, str, str, bool], Awaitable[Optional[User]]
]
AuthenticateUserFilter = Callable[
    [AuthenticateUserAction, GraphQLContext, str, str, bool], Awaitable[Optional[User]]
]


class AuthenticateUserHook(FilterHook[AuthenticateUserAction, AuthenticateUserFilter]):
    def call_action(
        self,
        action: AuthenticateUserAction,
        context: GraphQLContext,
        username: str,
        password: str,
        in_admin: bool,
    ) -> Awaitable[Optional[User]]:
        return self.filter(action, context, username, password, in_admin)


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


GetAuthUserAction = Callable[[GraphQLContext, int], Awaitable[Optional[User]]]
GetAuthUserFilter = Callable[
    [GetAuthUserAction, GraphQLContext, int], Awaitable[Optional[User]]
]


class GetAuthUserHook(FilterHook[GetAuthUserAction, GetAuthUserFilter]):
    def call_action(
        self,
        action: GetAuthUserAction,
        context: GraphQLContext,
        user_id: int,
        in_admin: bool = False,
    ) -> Awaitable[Optional[User]]:
        return self.filter(action, context, user_id, in_admin)


GetUserFromContextAction = Callable[[GraphQLContext, bool], Awaitable[Optional[User]]]
GetUserFromContextFilter = Callable[
    [GetUserFromContextAction, GraphQLContext, bool],
    Awaitable[Optional[User]],
]


class GetUserFromContextHook(
    FilterHook[GetUserFromContextAction, GetUserFromContextFilter]
):
    def call_action(
        self, action: GetUserFromContextAction, context: GraphQLContext, in_admin: bool
    ) -> Awaitable[Optional[User]]:
        return self.filter(action, context, in_admin)


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


authenticate_user_hook = AuthenticateUserHook()
create_user_token_hook = CreateUserTokenHook()
create_user_token_payload_hook = CreateUserTokenPayloadHook()
get_auth_user_hook = GetAuthUserHook()
get_user_from_context_hook = GetUserFromContextHook()
get_user_from_token_hook = GetUserFromTokenHook()
get_user_from_token_payload_hook = GetUserFromTokenPayloadHook()
