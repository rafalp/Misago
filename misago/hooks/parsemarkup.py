from typing import Awaitable, Tuple

from ..types import (
    GraphQLContext,
    ParsedMarkupMetadata,
    ParseMarkupAction,
    ParseMarkupFilter,
    RichText,
)
from .filter import FilterHook


class ParseMarkupHook(FilterHook[ParseMarkupAction, ParseMarkupFilter]):
    def call_action(
        self,
        action: ParseMarkupAction,
        context: GraphQLContext,
        markup: str,
        metadata: ParsedMarkupMetadata,
    ) -> Awaitable[Tuple[RichText, ParsedMarkupMetadata]]:
        return self.filter(action, context, markup, metadata)
