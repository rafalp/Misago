from typing import Optional

from ..types import (
    ConvertInlineAstToTextAction,
    ConvertInlineAstToTextFilter,
    GraphQLContext,
    ParsedMarkupMetadata,
)
from .filter import FilterHook


class ConvertInlineAstToTextHook(
    FilterHook[ConvertInlineAstToTextAction, ConvertInlineAstToTextFilter]
):
    is_async = False

    def call_action(
        self,
        action: ConvertInlineAstToTextAction,
        context: GraphQLContext,
        ast: dict,
        metadata: ParsedMarkupMetadata,
    ) -> Optional[str]:
        return self.filter(action, context, ast, metadata)
