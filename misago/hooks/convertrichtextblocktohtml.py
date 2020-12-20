from typing import Optional

from ..types import (
    ConvertRichTextBlockToHTMLAction,
    ConvertRichTextBlockToHTMLFilter,
    GraphQLContext,
    RichTextBlock,
)
from .filter import FilterHook


class ConvertRichTextBlockToHTMLHook(
    FilterHook[ConvertRichTextBlockToHTMLAction, ConvertRichTextBlockToHTMLFilter]
):
    is_async = False

    def call_action(
        self,
        action: ConvertRichTextBlockToHTMLAction,
        context: GraphQLContext,
        block: RichTextBlock,
    ) -> Optional[str]:
        return self.filter(action, context, block)
