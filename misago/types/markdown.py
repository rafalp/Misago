from typing import Protocol, List

from .graphqlcontext import GraphQLContext
from .parsemarkup import ParsedMarkupMetadata


class MarkdownAction(Protocol):
    def __call__(
        self, context: GraphQLContext, markup: str, metadata: ParsedMarkupMetadata
    ) -> List[dict]:
        ...


class MarkdownFilter(Protocol):
    def __call__(
        self,
        action: MarkdownAction,
        context: GraphQLContext,
        markup: str,
        metadata: ParsedMarkupMetadata,
    ) -> List[dict]:
        ...
