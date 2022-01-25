from typing import Any

from ..graphql import GraphQLContext
from .errors import NotAuthenticatedError


class IsAuthenticatedValidator:
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, data: Any, *_) -> Any:
        user = self._context["user"]
        if not user:
            raise NotAuthenticatedError()
        return data
