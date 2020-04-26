from starlette.requests import Request

from ..cacheversions import get_cache_versions
from ..conf.dynamicsettings import get_dynamic_settings
from ..types import GraphQLContext


async def get_graphql_context(request: Request) -> GraphQLContext:
    if request.scope["type"] == "websocket":
        cache_versions = await get_cache_versions()
        settings = await get_dynamic_settings(cache_versions)

        return {
            "request": request,
            "cache_versions": cache_versions,
            "settings": settings,
        }

    return {
        "request": request,
        "cache_versions": request.state.cache_versions,
        "settings": request.state.settings,
    }
