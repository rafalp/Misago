from typing import Callable, List, Protocol

from mistune import BlockParser, InlineParser, Markdown

from .graphqlcontext import GraphQLContext


MarkdownPlugin = Callable[[Markdown], None]


class CreateMarkdownAction(Protocol):
    def __call__(
        self,
        block: BlockParser,
        inline: InlineParser,
        plugins: List[MarkdownPlugin],
        context: GraphQLContext,
    ) -> Markdown:
        ...


class CreateMarkdownFilter(Protocol):
    def __call__(
        self,
        action: CreateMarkdownAction,
        block: BlockParser,
        inline: InlineParser,
        plugins: List[MarkdownPlugin],
        context: GraphQLContext,
    ) -> Markdown:
        ...
