from typing import Awaitable, Callable, Optional

from ...graphql import GraphQLContext
from ...hooks import FilterHook
from ...users.models import User

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


get_auth_user_hook = GetAuthUserHook()
