from typing import Protocol, Tuple

from .graphqlcontext import GraphQLContext
from .richtext import RichText


ParsedMarkupMetadata = dict


class ParseMarkupAction(Protocol):
    async def __call__(
        self, context: GraphQLContext, markup: str, metadata: ParsedMarkupMetadata
    ) -> Tuple[RichText, ParsedMarkupMetadata]:
        ...


class ParseMarkupFilter(Protocol):
    async def __call__(
        self,
        action: ParseMarkupAction,
        context: GraphQLContext,
        markup: str,
        metadata: ParsedMarkupMetadata,
    ) -> Tuple[RichText, ParsedMarkupMetadata]:
        ...
