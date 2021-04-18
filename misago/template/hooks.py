from typing import Any, Awaitable, Callable, Dict, List

from starlette.requests import Request

from ..hooks.filter import FilterHook
from .types import TemplateContext

TemplateContextAction = Callable[[Request], Awaitable[TemplateContext]]
TemplateContextFilter = Callable[
    [TemplateContextAction, Request], Awaitable[TemplateContext]
]


class TemplateContextHook(FilterHook[TemplateContextAction, TemplateContextFilter]):
    def call_action(
        self, action: TemplateContextAction, request: Request
    ) -> Awaitable[TemplateContext]:
        return self.filter(action, request)


template_context_hook = TemplateContextHook()

jinja2_extensions_hook: List[Any] = []
jinja2_filters_hook: Dict[str, Any] = {}
