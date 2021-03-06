from typing import Any, Awaitable, Callable, Dict

from .graphqlcontext import GraphQLContext
from .user import User

CreateUserTokenAction = Callable[[GraphQLContext, User, bool], Awaitable[str]]
CreateUserTokenFilter = Callable[
    [CreateUserTokenAction, GraphQLContext, User, bool], Awaitable[str]
]

CreateUserTokenPayloadAction = Callable[
    [GraphQLContext, User, bool], Awaitable[Dict[str, Any]]
]
CreateUserTokenPayloadFilter = Callable[
    [CreateUserTokenPayloadAction, GraphQLContext, User, bool],
    Awaitable[Dict[str, Any]],
]
