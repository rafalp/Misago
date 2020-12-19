from typing import List

from ..types import (
    GraphQLContext,
    MarkdownAction,
    MarkdownFilter,
)
from .filter import FilterHook


class MarkdownHook(FilterHook[MarkdownAction, MarkdownFilter]):
    is_async = False

    def call_action(
        self, action: MarkdownAction, context: GraphQLContext, markup: str,
    ) -> List[dict]:
        return self.filter(action, context, markup)
