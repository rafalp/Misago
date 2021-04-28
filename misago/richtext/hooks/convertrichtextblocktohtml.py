from typing import Optional, Protocol

from ...graphql import GraphQLContext
from ...hooks import FilterHook
from ..types import RichTextBlock


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


convert_rich_text_block_to_html_hook = ConvertRichTextBlockToHTMLHook()
