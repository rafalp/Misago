from typing import Protocol

from ...graphql import GraphQLContext
from ...hooks import FilterHook
from ..types import RichText


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


convert_rich_text_to_html_hook = ConvertRichTextToHTMLHook()
