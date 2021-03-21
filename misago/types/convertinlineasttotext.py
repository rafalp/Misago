from typing import Optional, Protocol

from .graphqlcontext import GraphQLContext
from .parsemarkup import ParsedMarkupMetadata


class ConvertInlineAstToTextAction(Protocol):
    def __call__(
        self,
        context: GraphQLContext,
        ast: dict,
        metadata: ParsedMarkupMetadata,
    ) -> Optional[str]:
        ...


class ConvertInlineAstToTextFilter(Protocol):
    def __call__(
        self,
        action: ConvertInlineAstToTextAction,
        context: GraphQLContext,
        ast: dict,
        metadata: ParsedMarkupMetadata,
    ) -> Optional[str]:
        ...
