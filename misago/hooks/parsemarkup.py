from typing import Tuple

from ..types import (
    GraphQLContext,
    ParsedMarkupMetadata,
    ParseMarkupAction,
    ParseMarkupFilter,
    RichText,
)
from .filter import FilterHook


class ParseMarkupHook(FilterHook[ParseMarkupAction, ParseMarkupFilter]):
    async def call_action(
        self,
        action: ParseMarkupAction,
        context: GraphQLContext,
        markup: str,
        metadata: ParsedMarkupMetadata,
    ) -> Tuple[RichText, ParsedMarkupMetadata]:
        return await self.filter(action, context, markup, metadata)
