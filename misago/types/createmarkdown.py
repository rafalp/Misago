from typing import Callable, List, Protocol

from mistune import BlockParser, InlineParser, Markdown

from .graphqlcontext import GraphQLContext


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
