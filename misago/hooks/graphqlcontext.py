from starlette.requests import Request

from ..types import GraphQLContext, GraphQLContextAction, GraphQLContextFilter
from .filter import FilterHook


class GraphQLContextHook(FilterHook[GraphQLContextAction, GraphQLContextFilter]):
    async def call_action(
        self, action: GraphQLContextAction, request: Request
    ) -> GraphQLContext:
        return await self.filter(action, request)
