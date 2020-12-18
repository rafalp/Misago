from typing import Protocol

from .graphqlcontext import GraphQLContext
from .parsemarkup import ParsedMarkupMetadata


class UpdateMarkupMetadataAction(Protocol):
    async def __call__(
        self, context: GraphQLContext, ast: dict, metadata: ParsedMarkupMetadata
    ):
        ...
