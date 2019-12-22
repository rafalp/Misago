from typing import Any, Awaitable, Callable, Dict, Optional

from .graphqlcontext import GraphQLContext
from .user import User


AuthenticateUserAction = Callable[[GraphQLContext, str, str], Awaitable[Optional[User]]]
AuthenticateUserFilter = Callable[
    [AuthenticateUserAction, GraphQLContext, str, str], Awaitable[Optional[User]]
]

GetAuthUserAction = Callable[[GraphQLContext, int], Awaitable[Optional[User]]]
GetAuthUserFilter = Callable[
    [GetAuthUserAction, GraphQLContext, int], Awaitable[Optional[User]]
]

GetUserFromContextAction = Callable[[GraphQLContext], Awaitable[Optional[User]]]
GetUserFromContextFilter = Callable[
    [GetUserFromContextAction, GraphQLContext], Awaitable[Optional[User]],
]

GetUserFromTokenAction = Callable[[GraphQLContext, str], Awaitable[Optional[User]]]
GetUserFromTokenFilter = Callable[
    [GetUserFromTokenAction, GraphQLContext, str], Awaitable[Optional[User]],
]

GetUserFromTokenPayloadAction = Callable[
    [GraphQLContext, Dict[str, Any]], Awaitable[Optional[User]]
]
GetUserFromTokenPayloadFilter = Callable[
    [GetUserFromTokenPayloadAction, GraphQLContext, Dict[str, Any]],
    Awaitable[Optional[User]],
]
