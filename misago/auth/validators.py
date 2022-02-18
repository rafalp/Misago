from typing import Any

from ..context import Context
from .errors import NotAuthenticatedError


class IsAuthenticatedValidator:
    _context: Context

    def __init__(self, context: Context):
        self._context = context

    async def __call__(self, data: Any, *_) -> Any:
        user = self._context["user"]
        if not user:
            raise NotAuthenticatedError()
        return data
