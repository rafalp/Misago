from typing import Any, Awaitable, Callable, Dict

from starlette.requests import Request


GraphQLContext = Dict[str, Any]
GraphQLContextAction = Callable[[Request], Awaitable[GraphQLContext]]
GraphQLContextFilter = Callable[
    [GraphQLContextAction, Request], Awaitable[GraphQLContext]
]
