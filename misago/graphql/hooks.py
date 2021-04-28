from typing import Awaitable, Callable, Dict, List, Type

from ariadne import SchemaBindable, SchemaDirectiveVisitor
from starlette.requests import Request

from ..hooks import FilterHook
from . import GraphQLContext

GraphQLContextAction = Callable[[Request], Awaitable[GraphQLContext]]
GraphQLContextFilter = Callable[
    [GraphQLContextAction, Request], Awaitable[GraphQLContext]
]


class GraphQLContextHook(FilterHook[GraphQLContextAction, GraphQLContextFilter]):
    def call_action(
        self, action: GraphQLContextAction, request: Request
    ) -> Awaitable[GraphQLContext]:
        return self.filter(action, request)


graphql_admin_directives_hook: Dict[str, Type[SchemaDirectiveVisitor]] = {}
graphql_admin_type_defs_hook: List[str] = []
graphql_admin_types_hook: List[SchemaBindable] = []
graphql_context_hook = GraphQLContextHook()
graphql_directives_hook: Dict[str, Type[SchemaDirectiveVisitor]] = {}
graphql_type_defs_hook: List[str] = []
graphql_types_hook: List[SchemaBindable] = []
