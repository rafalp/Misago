from typing import Awaitable, Callable

from starlette.requests import Request

from ..types import GraphQLContext
from .filter import FilterHook

GraphQLContextAction = Callable[[Request], Awaitable[GraphQLContext]]
GraphQLContextFilter = Callable[
    [GraphQLContextAction, Request], Awaitable[GraphQLContext]
]


class GraphQLContextHook(FilterHook[GraphQLContextAction, GraphQLContextFilter]):
    def call_action(
        self, action: GraphQLContextAction, request: Request
    ) -> Awaitable[GraphQLContext]:
        return self.filter(action, request)
