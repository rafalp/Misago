from typing import Any, Callable, Coroutine, Dict

from starlette.requests import Request


GraphQLContext = Dict[str, Any]
GraphQLContextAction = Callable[
    [Request, GraphQLContext], Coroutine[Any, Any, GraphQLContext]
]
GraphQLContextFilter = Callable[
    [GraphQLContextAction, Request, GraphQLContext], Coroutine[Any, Any, GraphQLContext]
]
