from typing import Awaitable

from starlette.requests import Request

from ..types import TemplateContext, TemplateContextAction, TemplateContextFilter
from .filter import FilterHook


class TemplateContextHook(FilterHook[TemplateContextAction, TemplateContextFilter]):
    def call_action(
        self, action: TemplateContextAction, request: Request
    ) -> Awaitable[TemplateContext]:
        return self.filter(action, request)
