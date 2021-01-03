from typing import List

from ..types import (
    GraphQLContext,
    ParsedMarkupMetadata,
    UpdateMarkupMetadataAction,
    UpdateMarkupMetadataFilter,
)
from .filter import FilterHook


class UpdateMarkupMetadataHook(
    FilterHook[UpdateMarkupMetadataAction, UpdateMarkupMetadataFilter]
):
    def call_action(
        self,
        action: UpdateMarkupMetadataAction,
        context: GraphQLContext,
        ast: List[dict],
        metadata: ParsedMarkupMetadata,
    ):
        return self.filter(action, context, ast, metadata)
