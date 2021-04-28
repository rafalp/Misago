from typing import Callable, List, Protocol

from mistune import BlockParser, InlineParser, Markdown

from ...graphql import GraphQLContext
from ...hooks import FilterHook

MarkdownPlugin = Callable[[Markdown], None]


class CreateMarkdownAction(Protocol):
    def __call__(
        self,
        context: GraphQLContext,
        block: BlockParser,
        inline: InlineParser,
        plugins: List[MarkdownPlugin],
    ) -> Markdown:
        ...


class CreateMarkdownFilter(Protocol):
    def __call__(
        self,
        action: CreateMarkdownAction,
        context: GraphQLContext,
        block: BlockParser,
        inline: InlineParser,
        plugins: List[MarkdownPlugin],
    ) -> Markdown:
        ...


class CreateMarkdownHook(FilterHook[CreateMarkdownAction, CreateMarkdownFilter]):
    is_async = False

    def call_action(
        self,
        action: CreateMarkdownAction,
        context: GraphQLContext,
        block: BlockParser,
        inline: InlineParser,
        plugins: List[MarkdownPlugin],
    ) -> Markdown:
        return self.filter(action, context, block, inline, plugins)


create_markdown_hook = CreateMarkdownHook()
