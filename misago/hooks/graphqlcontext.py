from typing import Awaitable

from starlette.requests import Request

from ..types import GraphQLContext, GraphQLContextAction, GraphQLContextFilter
from .filter import FilterHook


class GraphQLContextHook(FilterHook[GraphQLContextAction, GraphQLContextFilter]):
    def call_action(
        self, action: GraphQLContextAction, request: Request
    ) -> Awaitable[GraphQLContext]:
        return self.filter(action, request)
