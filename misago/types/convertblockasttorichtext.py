from typing import Optional, Protocol

from .graphqlcontext import GraphQLContext
from .richtext import RichTextBlock


class ConvertBlockAstToRichTextAction(Protocol):
    def __call__(self, context: GraphQLContext, ast: dict,) -> Optional[RichTextBlock]:
        ...


class ConvertBlockAstToRichTextFilter(Protocol):
    def __call__(
        self,
        action: ConvertBlockAstToRichTextAction,
        context: GraphQLContext,
        ast: dict,
    ) -> Optional[RichTextBlock]:
        ...
