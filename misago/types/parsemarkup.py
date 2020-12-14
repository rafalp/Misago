from typing import Protocol

from .graphqlcontext import GraphQLContext
from .richtext import RichText


class ParseMarkupAction(Protocol):
    async def __call__(self, context: GraphQLContext, markup: str,) -> RichText:
        ...


class ParseMarkupFilter(Protocol):
    async def __call__(
        self, action: ParseMarkupAction, context: GraphQLContext, markup: str,
    ) -> RichText:
        ...
