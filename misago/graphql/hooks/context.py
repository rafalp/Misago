from typing import Awaitable, Callable

from starlette.requests import Request

from ...context import Context
from ...hooks import FilterHook

ContextAction = Callable[[Request], Awaitable[Context]]
ContextFilter = Callable[[ContextAction, Request], Awaitable[Context]]


class ContextHook(FilterHook[ContextAction, ContextFilter]):
    def call_action(
        self, action: ContextAction, request: Request
    ) -> Awaitable[Context]:
        return self.filter(action, request)


graphql_context_hook = ContextHook()
