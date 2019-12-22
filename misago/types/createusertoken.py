from typing import Any, Awaitable, Callable, Dict

from .graphqlcontext import GraphQLContext
from .user import User


CreateUserTokenAction = Callable[[GraphQLContext, User], Awaitable[str]]
CreateUserTokenFilter = Callable[
    [CreateUserTokenAction, GraphQLContext, User], Awaitable[str]
]

CreateUserTokenPayloadAction = Callable[
    [GraphQLContext, User], Awaitable[Dict[str, Any]]
]
CreateUserTokenPayloadFilter = Callable[
    [CreateUserTokenPayloadAction, GraphQLContext, User], Awaitable[Dict[str, Any]],
]
