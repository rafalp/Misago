from typing import List

from mistune import BlockParser, InlineParser, Markdown

from ..types import (
    CreateMarkdownAction,
    CreateMarkdownFilter,
    GraphQLContext,
    MarkdownPlugin,
)
from .filter import FilterHook


class CreateMarkdownHook(FilterHook[CreateMarkdownAction, CreateMarkdownFilter]):
    is_async = False

    def call_action(
        self,
        action: CreateMarkdownAction,
        block: BlockParser,
        inline: InlineParser,
        plugins: List[MarkdownPlugin],
        context: GraphQLContext,
    ) -> Markdown:
        return self.filter(action, block, inline, plugins, context,)
