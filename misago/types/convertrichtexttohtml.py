from typing import Protocol

from .graphqlcontext import GraphQLContext
from .richtext import RichText


class ConvertRichTextToHTMLAction(Protocol):
    def __call__(self, context: GraphQLContext, rich_text: RichText) -> str:
        ...


class ConvertRichTextToHTMLFilter(Protocol):
    def __call__(
        self,
        action: ConvertRichTextToHTMLAction,
        context: GraphQLContext,
        rich_text: RichText,
    ) -> str:
        ...
