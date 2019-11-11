from starlette.requests import Request

from ..cacheversions import get_cache_versions
from ..types import GraphQLContext


async def get_graphql_context(_: Request, context: GraphQLContext) -> GraphQLContext:
    cache_versions = await get_cache_versions()
    context.update({"cache_versions": cache_versions})
    return context
