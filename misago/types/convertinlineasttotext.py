from typing import Optional, Protocol

from .graphqlcontext import GraphQLContext


class ConvertInlineAstToTextAction(Protocol):
    def __call__(self, context: GraphQLContext, ast: dict,) -> Optional[str]:
        ...


class ConvertInlineAstToTextFilter(Protocol):
    def __call__(
        self, action: ConvertInlineAstToTextAction, context: GraphQLContext, ast: dict,
    ) -> Optional[str]:
        ...
