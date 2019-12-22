from typing import Any, Awaitable, Dict, Callable

from starlette.requests import Request


TemplateContext = Dict[str, Any]
TemplateContextAction = Callable[[Request], Awaitable[TemplateContext]]
TemplateContextFilter = Callable[
    [TemplateContextAction, Request], Awaitable[TemplateContext]
]
