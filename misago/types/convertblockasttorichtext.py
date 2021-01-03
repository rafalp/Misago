from typing import Optional, Protocol

from .graphqlcontext import GraphQLContext
from .parsemarkup import ParsedMarkupMetadata
from .richtext import RichTextBlock


class ConvertBlockAstToRichTextAction(Protocol):
    def __call__(
        self, context: GraphQLContext, ast: dict, metadata: ParsedMarkupMetadata
    ) -> Optional[RichTextBlock]:
        ...


class ConvertBlockAstToRichTextFilter(Protocol):
    def __call__(
        self,
        action: ConvertBlockAstToRichTextAction,
        context: GraphQLContext,
        ast: dict,
        metadata: ParsedMarkupMetadata,
    ) -> Optional[RichTextBlock]:
        ...
