from typing import Protocol, List

from .graphqlcontext import GraphQLContext


class MarkdownAction(Protocol):
    def __call__(self, context: GraphQLContext, markup: str) -> List[dict]:
        ...


class MarkdownFilter(Protocol):
    def __call__(
        self, action: MarkdownAction, context: GraphQLContext, markup: str,
    ) -> List[dict]:
        ...
