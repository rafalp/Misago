from ..types import (
    ConvertRichTextToHTMLAction,
    ConvertRichTextToHTMLFilter,
    GraphQLContext,
    RichText,
)
from .filter import FilterHook


class ConvertRichTextToHTMLHook(
    FilterHook[ConvertRichTextToHTMLAction, ConvertRichTextToHTMLFilter]
):
    is_async = False

    def call_action(
        self,
        action: ConvertRichTextToHTMLAction,
        context: GraphQLContext,
        rich_text: RichText,
    ) -> str:
        return self.filter(action, context, rich_text)
