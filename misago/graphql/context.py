from dataclasses import dataclass

from starlette.requests import Request

from ..auth import get_authenticated_admin, get_authenticated_user
from ..cacheversions import get_cache_versions
from ..conf.dynamicsettings import get_dynamic_settings
from ..threads.loaders import posts_loader, threads_loader
from . import GraphQLContext
from .hooks import graphql_context_hook


@dataclass
class Space:
    admin: bool
    public: bool


async def get_graphql_context(request: Request) -> GraphQLContext:
    request.scope["user"] = None

    context = {
        "request": request,
        "user": None,
    }

    if request.scope["type"] == "websocket":
        cache_versions = await get_cache_versions()
        settings = await get_dynamic_settings(cache_versions)

        context.update(
            {
                "cache_versions": cache_versions,
                "settings": settings,
            }
        )
    else:
        context.update(
            {
                "cache_versions": request.state.cache_versions,
                "settings": request.state.settings,
            }
        )

    threads_loader.setup_context(context)
    posts_loader.setup_context(context)

    return context


async def get_public_graphql_context(request: Request) -> GraphQLContext:
    return await graphql_context_hook.call_action(
        get_public_graphql_context_action, request
    )


async def get_public_graphql_context_action(request: Request) -> GraphQLContext:
    context = await get_graphql_context(request)
    context["space"] = Space(admin=False, public=True)
    context["user"] = await get_authenticated_user(context)
    request.scope["user"] = context["user"]
    return context


async def get_admin_graphql_context(request: Request) -> GraphQLContext:
    return await graphql_context_hook.call_action(
        get_admin_graphql_context_action, request
    )


async def get_admin_graphql_context_action(request: Request) -> GraphQLContext:
    context = await get_graphql_context(request)
    context["space"] = Space(admin=True, public=False)
    context["user"] = await get_authenticated_admin(context)
    request.scope["user"] = context["user"]
    return context
