from starlette.requests import Request

from ..types import TemplateContext, TemplateContextAction, TemplateContextFilter
from .filter import FilterHook


class TemplateContextHook(FilterHook[TemplateContextAction, TemplateContextFilter]):
    async def call_action(
        self, action: TemplateContextAction, request: Request
    ) -> TemplateContext:
        return await self.filter(action, request)
