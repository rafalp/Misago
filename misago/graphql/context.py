from starlette.requests import Request

from ..types import GraphQLContext


async def get_graphql_context(request: Request) -> GraphQLContext:
    return {
        "request": request,
        "cache_versions": request.state.cache_versions,
        "settings": request.state.settings,
    }
