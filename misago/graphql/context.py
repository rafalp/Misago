from starlette.requests import Request

from ..cacheversions import get_cache_versions
from ..conf.dynamicsettings import get_dynamic_settings
from ..types import GraphQLContext


async def get_graphql_context(
    request: Request, context: GraphQLContext
) -> GraphQLContext:
    cache_versions = await get_cache_versions()
    settings = await get_dynamic_settings(cache_versions)

    context.update(
        {
            "cache_versions": cache_versions,
            "request": request,
            "settings": settings.items(),
        }
    )

    return context
