from typing import Awaitable, Callable, Optional

from ...graphql import GraphQLContext
from ...hooks import FilterHook
from ...users.models import User

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


get_user_from_context_hook = GetUserFromContextHook()
