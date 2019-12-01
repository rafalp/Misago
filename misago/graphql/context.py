from starlette.requests import Request

from ..cacheversions import get_cache_versions
from ..conf.dynamicsettings import get_dynamic_settings
from ..types import GraphQLContext


async def get_graphql_context(request: Request) -> GraphQLContext:
    cache_versions = await get_cache_versions()
    return {
        "cache_versions": cache_versions,
        "request": request,
        "settings": await get_dynamic_settings(cache_versions),
    }
