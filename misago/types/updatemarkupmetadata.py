from typing import List, Protocol

from .graphqlcontext import GraphQLContext
from .parsemarkup import ParsedMarkupMetadata


class UpdateMarkupMetadataAction(Protocol):
    async def __call__(
        self, context: GraphQLContext, ast: List[dict], metadata: ParsedMarkupMetadata
    ):
        ...
