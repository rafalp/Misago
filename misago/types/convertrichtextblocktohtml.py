from typing import Optional, Protocol

from .graphqlcontext import GraphQLContext
from .richtext import RichTextBlock


class ConvertRichTextBlockToHTMLAction(Protocol):
    def __call__(self, context: GraphQLContext, block: RichTextBlock) -> Optional[str]:
        ...


class ConvertRichTextBlockToHTMLFilter(Protocol):
    def __call__(
        self,
        action: ConvertRichTextBlockToHTMLAction,
        context: GraphQLContext,
        block: RichTextBlock,
    ) -> Optional[str]:
        ...
