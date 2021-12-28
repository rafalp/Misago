from functools import partial
from typing import Optional

from starlette.requests import Request

from ..richtext import convert_rich_text_to_html
from .hooks import template_context_hook
from .types import TemplateContext


async def get_final_context(
    request: Request, context: Optional[TemplateContext] = None
) -> TemplateContext:
    final_context = await template_context_hook.call_action(
        get_default_context, request
    )
    if context:
        final_context.update(context)
    return final_context


async def get_default_context(request: Request) -> TemplateContext:
    render_rich_text = partial(convert_rich_text_to_html, request)

    return {
        "request": request,
        "render_rich_text": render_rich_text,
        "settings": request.state.settings,
        "cache_versions": request.state.cache_versions,
    }
