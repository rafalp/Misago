from typing import List

from ..types import (
    GraphQLContext,
    MarkdownAction,
    MarkdownFilter,
    ParsedMarkupMetadata,
)
from .filter import FilterHook


class MarkdownHook(FilterHook[MarkdownAction, MarkdownFilter]):
    is_async = False

    def call_action(
        self,
        action: MarkdownAction,
        context: GraphQLContext,
        markup: str,
        metadata: ParsedMarkupMetadata,
    ) -> List[dict]:
        return self.filter(action, context, markup, metadata)
