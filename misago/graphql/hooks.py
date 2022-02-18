from typing import Awaitable, Callable, Dict, List, Type

from ariadne import SchemaBindable, SchemaDirectiveVisitor
from starlette.requests import Request

from ..context import Context
from ..hooks import FilterHook

ContextAction = Callable[[Request], Awaitable[Context]]
ContextFilter = Callable[[ContextAction, Request], Awaitable[Context]]


class ContextHook(FilterHook[ContextAction, ContextFilter]):
    def call_action(
        self, action: ContextAction, request: Request
    ) -> Awaitable[Context]:
        return self.filter(action, request)


graphql_admin_directives_hook: Dict[str, Type[SchemaDirectiveVisitor]] = {}
graphql_admin_type_defs_hook: List[str] = []
graphql_admin_types_hook: List[SchemaBindable] = []
graphql_context_hook = ContextHook()
graphql_directives_hook: Dict[str, Type[SchemaDirectiveVisitor]] = {}
graphql_type_defs_hook: List[str] = []
graphql_types_hook: List[SchemaBindable] = []
